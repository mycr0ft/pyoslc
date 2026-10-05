# -*- coding: utf-8 -*-
"""Vee-link registry (P3): maps element identity across the SE Vee.

The join table ties a SysML element's declared qualified name and its
stable interchange ``@id`` (sysmlpy ``qn_registry`` output) to the
STEP-domain resources that realize it (``StepProduct`` /
``StepProductDefinition`` / ``StepShapeRepresentation``), plus the
reverse direction.

Links are stored as one entry per cross-edge:

    SysML QN 'SaturnV.Engine'  <--->  STEP step:Product '#4374'

with an optional link kind (``realizes`` | ``specifies`` | ``traces``
— the OSLC RM vocabulary's relationship kinds) and provenance
(who/when recorded by the business layer).

Persistence: in-memory by default (mirror of the resource repo); a
JSON sidecar keeps the links across restarts — the same shape as
sysmlpy's reconcile registry (the export file doubles as the join
registry), so a CI job can regenerate the STEP side and only the
links file needs to survive.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from typing import Dict, List, Optional

from .repository import get_step_repository
from pyoslc.resources.domains.step import (
    StepProduct, StepProductDefinition, StepShapeRepresentation,
)

# OSLC RM-ish link kinds (kept as plain strings; the vocabulary is
# external — the registry does not pin OSLC constants for these)
LINK_KINDS = ("realizes", "specifies", "traces")

_SYSML_QN_KEY = "sysml_qn"
_SYSML_ID_KEY = "sysml_id"


@dataclass
class VeeLink:
    """One identity edge between the SysML and STEP worlds."""

    sysml_qn: str                    # declared qualified name ('P.Engine')
    sysml_id: str                    # stable interchange @id ('sysml:…')
    step_ref: str                    # STEP instance ref ('#4374')
    step_resource_id: str            # repository identifier ('4374')
    kind: str = "realizes"

    def to_dict(self) -> dict:
        return {
            "sysml_qn": self.sysml_qn,
            "sysml_id": self.sysml_id,
            "step_ref": self.step_ref,
            "step_resource_id": self.step_resource_id,
            "kind": self.kind,
        }


class VeeRegistry:
    """The SysML<->STEP link table (with an optional JSON sidecar)."""

    def __init__(self, title: str = "vee-registry", sidecar: str = ""):
        self.title = title
        self.sidecar = sidecar
        self._by_sysml: Dict[str, List[VeeLink]] = {}
        self._by_step: Dict[str, List[VeeLink]] = {}

    # -- CRUD ---------------------------------------------------------
    def link(self, sysml_qn: str, sysml_id: str, step_ref: str,
             step_resource_id: str, kind: str = "realizes") -> VeeLink:
        if kind not in LINK_KINDS:
            raise ValueError(f"link kind must be one of {LINK_KINDS}, "
                             f"got {kind!r}")
        # one link per (sysml element, step element) pair — an element
        # may realize several STEP parts and vice versa, but never the
        # same pair twice
        for existing in self._by_sysml.get(sysml_qn, []):
            if existing.step_ref == step_ref and existing.kind == kind:
                return existing
        link = VeeLink(sysml_qn, sysml_id, step_ref, step_resource_id, kind)
        self._by_sysml.setdefault(sysml_qn, []).append(link)
        self._by_step.setdefault(step_ref, []).append(link)
        return link

    def unlink(self, sysml_qn: str, step_ref: str,
               kind: Optional[str] = None) -> bool:
        removed = False
        for lst, _ in ((self._by_sysml, None), (self._by_step, None)):
            pass
        # remove from both indexes
        for lst in (self._by_sysml.get(sysml_qn, []),
                    self._by_step.get(step_ref, [])):
            keep = [l for l in lst
                    if not (l.sysml_qn == sysml_qn and l.step_ref == step_ref
                            and (kind is None or l.kind == kind))]
            if len(keep) != len(lst):
                removed = True
            lst[:] = keep
        return removed

    # -- queries -------------------------------------------------------
    def by_sysml(self, sysml_qn: str) -> List[VeeLink]:
        return list(self._by_sysml.get(sysml_qn, []))

    def by_step(self, step_ref: str) -> List[VeeLink]:
        return list(self._by_step.get(step_ref, []))

    def all(self) -> List[VeeLink]:
        seen, out = set(), []
        for lst in self._by_sysml.values():
            for l in lst:
                key = (l.sysml_qn, l.step_ref, l.kind)
                if key not in seen:
                    seen.add(key)
                    out.append(l)
        return out

    # -- import from the SysML side (qn_registry output) ---------------
    def ingest_qn_registry(self, qn_map: dict, match_by_name=None) -> int:
        """Auto-link SysML elements to STEP resources by declared name.

        qn_map: sysmlpy ``qn_registry`` output —
            ``{'SaturnV.Engine': 'sysml:…', …}``
        match_by_name: optional callable(step_resource) -> str giving
            the SysML leaf-name to try; default = the resource title.
        Returns the number of NEW links.
        """
        repo = get_step_repository()
        new = 0
        resources = (repo.list_by_type(StepProduct)
                     + repo.list_by_type(StepProductDefinition))
        for r in resources:
            leaf = (match_by_name(r) if match_by_name
                    else (r.title or "").strip().lower())
            if not leaf:
                continue
            for qn, sid in qn_map.items():
                qn_leaf = qn.rsplit(".", 1)[-1].strip("'\"").strip().lower()
                if qn_leaf == leaf:
                    before = len(self.by_sysml(qn))
                    self.link(qn, sid, r.source_ref or "#" + r.identifier,
                              r.identifier)
                    if len(self.by_sysml(qn)) > before:
                        new += 1
        return new

    # -- persistence ---------------------------------------------------
    def save(self) -> Optional[str]:
        if not self.sidecar:
            return None
        with open(self.sidecar, "w", encoding="utf-8") as fh:
            json.dump([l.to_dict() for l in self.all()], fh, indent=1)
        return self.sidecar

    def load(self) -> int:
        if not self.sidecar:
            return 0
        try:
            with open(self.sidecar, encoding="utf-8") as fh:
                rows = json.load(fh)
        except FileNotFoundError:
            return 0
        n = 0
        for row in rows:
            self.link(row["sysml_qn"], row["sysml_id"], row["step_ref"],
                      row["step_resource_id"], row.get("kind", "realizes"))
            n += 1
        return n


_registry: Optional[VeeRegistry] = None


def get_vee_registry() -> VeeRegistry:
    global _registry
    if _registry is None:
        _registry = VeeRegistry()
    return _registry


def set_vee_registry(registry: Optional[VeeRegistry]) -> None:
    global _registry
    _registry = registry