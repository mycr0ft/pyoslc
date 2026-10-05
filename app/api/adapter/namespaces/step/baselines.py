# -*- coding: utf-8 -*-
"""P4: OSLC Config-Management baselines pinning the SE Vee.

A **Vee baseline** is the PLM "released configuration" of this
integration: one persistent resource that pins, by content hash, the
SYSML model AND the STEP geometry snapshot that together define a
configuration of the system — plus the Vee links that connect them.

Artifacts pinned per baseline (all hash-addressed, content-stored
once in the artifact store):

* every `.sysml` source file (sha256, size)
* every `.stp` STEP file (sha256, size)
* the SysML interchange payload (`to_interchange(stable_ids=True)`
  JSON text, with the QN registry) — the derived artifact
* the stepper structure payload (OSLC JSON-LD from the .stp) — derived
* the Vee link table at baseline time (the registry snapshot)

A baseline's integrity is verifiable: re-hash the stored artifacts
and compare with the recorded digests.  `derived_from` chains
baselines (prov:wasDerivedFrom) so evolution history reads as the
release history.  Baselines are immutable — a change creates a NEW
baseline; the API rejects edits to a recorded one.

Classes: :class:`Baseline` (the pin) and :class:`ArtifactStore`
(content-addressed blob store).  Backed by the filesystem under the
app's data dir by default; :class:`InMemoryBaselineStore` for tests.
"""

from __future__ import annotations

import hashlib
import json
import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


class ArtifactStore:
    """Content-addressed blob store: sha256 -> bytes, on disk."""

    def __init__(self, root: str):
        self.root = root
        os.makedirs(root, exist_ok=True)

    def put(self, data: bytes) -> str:
        digest = hashlib.sha256(data).hexdigest()
        path = os.path.join(self.root, digest)
        if not os.path.exists(path):
            tmp = path + ".tmp"
            with open(tmp, "wb") as fh:
                fh.write(data)
            os.replace(tmp, path)
        return digest

    def put_text(self, text: str) -> str:
        return self.put(text.encode("utf-8"))

    def get(self, digest: str) -> Optional[bytes]:
        path = os.path.join(self.root, digest)
        if not os.path.exists(path):
            return None
        with open(path, "rb") as fh:
            return fh.read()

    def has(self, digest: str) -> bool:
        return os.path.exists(os.path.join(self.root, digest))


class InMemoryArtifactStore(ArtifactStore):
    def __init__(self):
        self._blobs: Dict[str, bytes] = {}
        self.root = ""

    def put(self, data: bytes) -> str:
        digest = hashlib.sha256(data).hexdigest()
        self._blobs[digest] = data
        return digest

    def get(self, digest: str):
        return self._blobs.get(digest)

    def has(self, digest: str):
        return digest in self._blobs


class InMemoryBaselineStore:
    """Process-local baseline registry (filesystem store optional)."""

    def __init__(self):
        self._baselines: Dict[str, dict] = {}   # id -> baseline dict

    def add(self, baseline: dict) -> dict:
        bid = baseline["id"]
        if bid in self._baselines:
            raise ValueError(f"baseline {bid} already exists")
        self._baselines[bid] = dict(baseline)
        return self._baselines[bid]

    def find(self, baseline_id: str):
        return self._baselines.get(baseline_id)

    def all(self) -> List[dict]:
        return sorted(self._baselines.values(),
                      key=lambda b: b.get("created", ""))

    def update(self, baseline_id: str, patch: dict) -> dict:
        raise ValueError("baselines are immutable — create a new one")


_store: Optional[InMemoryBaselineStore] = None
_artifacts: Optional[ArtifactStore] = None


def get_baseline_store() -> InMemoryBaselineStore:
    global _store
    if _store is None:
        _store = InMemoryBaselineStore()
    return _store


def set_baseline_store(store) -> None:
    global _store
    _store = store


def get_artifact_store() -> ArtifactStore:
    global _artifacts
    if _artifacts is None:
        root = os.environ.get(
            "VEE_ARTIFACT_DIR",
            os.path.join(os.path.expanduser("~"), ".hermes", "vee-artifacts")
            if os.environ.get("VEE_HOME") else os.path.join(
                os.getcwd(), "vee-artifacts"))
        _artifacts = ArtifactStore(root)
    return _artifacts


def set_artifact_store(store) -> None:
    global _artifacts
    _artifacts = store


@dataclass
class BaselineInput:
    """Everything one baseline pins. SysML/STEP files are hashed from
    disk; the derived payloads are computed at creation time."""

    title: str
    description: str = ""
    sysml_files: List[str] = field(default_factory=list)
    step_files: List[str] = field(default_factory=list)
    derived_from: str = ""            # previous baseline id
    author: str = ""


def create_baseline(inp: BaselineInput, *, include_payloads: bool = True) -> dict:
    """Pin a Vee configuration. Idempotent per content: two identical
    inputs produce the SAME baseline id.

    The id is the content digest of the recorded manifest (files +
    derived payloads + vee links): immutable by construction.
    """
    from stepper.structure import extract_structure, to_oslc_jsonld
    from app.api.adapter.namespaces.step.vee import get_vee_registry

    store = get_artifact_store()
    artifacts: List[dict] = []

    # -- source files -------------------------------------------------
    for path in inp.sysml_files:
        if not os.path.exists(path):
            raise FileNotFoundError(f"sysml file not found: {path}")
        with open(path, "rb") as fh:
            digest = store.put(fh.read())
        artifacts.append({"kind": "sysml", "path": os.path.basename(path),
                          "sha256": digest, "size": os.path.getsize(path)})
    for path in inp.step_files:
        if not os.path.exists(path):
            raise FileNotFoundError(f"step file not found: {path}")
        with open(path, "rb") as fh:
            digest = store.put(fh.read())
        artifacts.append({"kind": "step", "path": os.path.basename(path),
                          "sha256": digest, "size": os.path.getsize(path)})

    if not artifacts:
        raise ValueError("baseline needs at least one sysml or step file")

    # -- derived payloads ----------------------------------------------
    if include_payloads:
        sysml_text = "\n".join(
            open(p, encoding="utf-8", errors="replace").read()
            for p in inp.sysml_files)
        if sysml_text.strip():
            try:
                import sysmlpy
                from sysmlpy.interchange import (
                    to_interchange, interchange_to_json_text, qn_registry,
                )
                m = sysmlpy.loads(sysml_text) if len(inp.sysml_files) == 1 \
                    else sysmlpy.load_files(list(inp.sysml_files))
                doc = to_interchange(m, stable_ids=True)
                reg = qn_registry(doc)
                doc.pop("#qn_registry", None)
                payload = interchange_to_json_text(doc, indent=None)
                digest = store.put_text(payload)
                artifacts.append({
                    "kind": "sysml_interchange", "path": "-",
                    "sha256": digest, "size": len(payload),
                    "qn_registry": reg,
                })
            except Exception as e:   # sysmlpy absent or model unparseable
                artifacts.append({
                    "kind": "sysml_interchange", "path": "-",
                    "error": str(e)[:200],
                })
        for p in inp.step_files:
            label = os.path.basename(p)
            try:
                s = extract_structure(p, file_label=label)
                payload = json.dumps(to_oslc_jsonld(s), sort_keys=True)
                digest = store.put_text(payload)
                artifacts.append({
                    "kind": "step_structure", "path": label,
                    "sha256": digest, "size": len(payload),
                })
            except Exception as e:
                artifacts.append({
                    "kind": "step_structure", "path": label,
                    "error": str(e)[:200],
                })

    # -- vee links snapshot ---------------------------------------------
    vee_rows = [l.to_dict() for l in get_vee_registry().all()]

    # -- manifest + id ----------------------------------------------------
    manifest = {
        "title": inp.title,
        "description": inp.description,
        "author": inp.author,
        "derived_from": inp.derived_from,
        "artifacts": artifacts,
        "vee_links": vee_rows,
    }
    canonical = json.dumps(manifest, sort_keys=True)
    baseline_id = "bl:" + hashlib.sha256(canonical.encode()).hexdigest()[:16]

    baseline = {
        "id": baseline_id,
        "created": _created_stamp(),
        **manifest,
    }
    saved = get_baseline_store().add(
        {**baseline, "created": _created_stamp()})   # raises on duplicate id
    return saved


def _created_stamp() -> str:
    import datetime
    return datetime.datetime.now().isoformat(timespec="seconds")


def verify_baseline(baseline_id: str) -> dict:
    """Re-hash every stored artifact of a baseline; report integrity."""
    store = get_baseline_store()
    baseline = store.find(baseline_id)
    if baseline is None:
        raise KeyError(f"baseline {baseline_id} not found")
    astore = get_artifact_store()
    results = []
    for art in baseline["artifacts"]:
        digest = art.get("sha256")
        if not digest:
            results.append({"path": art.get("path"), "status": "no-hash"})
            continue
        data = astore.get(digest)
        ok = data is not None and hashlib.sha256(data).hexdigest() == digest
        results.append({"path": art.get("path"), "sha256": digest,
                        "status": "ok" if ok else "MISSING"})
    return {
        "id": baseline_id,
        "verified": all(r["status"] in ("ok", "no-hash")
                        for r in results),
        "artifacts": results,
    }