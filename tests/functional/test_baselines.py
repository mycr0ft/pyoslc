# -*- coding: utf-8 -*-
"""P4 functional tests: Vee baselines (OSLC Config Management).

Chain under test:
  create_baseline(BaselineInput(sysml_files, step_files))
    -> ArtifactStore pins source bytes by sha256
    -> derives the sysml interchange payload (stable_ids, needs
       sysmlpy) and the stepper structure payload per .stp
    -> snapshots the Vee link table
    -> manifest digest = immutable baseline id ('bl:<16 hex>')
  /oslc/step/baselines REST — list/create/get/verify

Immutability is the CONFIG-MGMT contract: re-creating identical
content raises (same id already recorded); editing is rejected;
integrity verification re-hashes the stored bytes.

Requires sysmlpy + stepper importable (editable installs).
"""

import json
import os

import pytest

from app.api.adapter.namespaces.step.baselines import (
    ArtifactStore, BaselineInput, InMemoryArtifactStore,
    InMemoryBaselineStore, create_baseline, get_artifact_store,
    get_baseline_store, set_artifact_store, set_baseline_store,
    verify_baseline,
)

HOME = os.path.expanduser("~")
SYSML_DIR = f"{HOME}/proj/pyoslc/examples/saturn_v/sysml"
NIST = ("/home/jfox/.hermes/cache/scratch/nist/NIST-PMI-STEP-Files/"
        "nist_ctc_01_asme1_ap242-e1.stp")

pytest.importorskip("sysmlpy")
pytest.importorskip("stepper")


@pytest.fixture
def env(tmp_path):
    set_baseline_store(InMemoryBaselineStore())
    set_artifact_store(InMemoryArtifactStore())
    yield
    set_baseline_store(None)
    set_artifact_store(None)


def _system_package():
    return os.path.join(SYSML_DIR, "SystemPackage.sysml")


class TestCreateBaseline:
    def test_files_pinned_by_hash(self, env):
        b = create_baseline(BaselineInput(
            title="t1", sysml_files=[_system_package()]))
        sysml_art = next(a for a in b["artifacts"] if a["kind"] == "sysml")
        import hashlib
        disk_digest = hashlib.sha256(
            open(_system_package(), "rb").read()).hexdigest()
        assert sysml_art["sha256"] == disk_digest
        # the artifact store holds the bytes
        assert get_artifact_store().get(disk_digest) == \
            open(_system_package(), "rb").read()

    def test_derived_payloads_recorded(self, env):
        b = create_baseline(BaselineInput(
            title="t2", sysml_files=[_system_package()],
            step_files=[NIST]))
        kinds = {a["kind"] for a in b["artifacts"]}
        assert {"sysml", "step", "sysml_interchange",
                "step_structure"} <= kinds
        # the interchange artifact carries the qn registry
        inter = next(a for a in b["artifacts"]
                     if a["kind"] == "sysml_interchange")
        assert isinstance(inter.get("qn_registry"), dict)
        # single-file load: SystemPackage's imports don't resolve, so
        # only its own subtree appears (8 elements); loading all four
        # Saturn V packages resolves ~100 elements — pinned separately
        assert len(inter["qn_registry"]) >= 8

    def test_no_files_400(self, env):
        with pytest.raises(ValueError):
            create_baseline(BaselineInput(title="empty"))

    def test_multi_file_model_resolves_cross_package(self, env):
        """The realistic load: all four Saturn V packages together —
        cross-package imports resolve and the qn registry grows
        accordingly."""
        files = sorted(
            os.path.join(SYSML_DIR, f)
            for f in os.listdir(SYSML_DIR) if f.endswith(".sysml"))
        assert len(files) == 4
        b = create_baseline(BaselineInput(
            title="full-saturnv", sysml_files=files, step_files=[NIST]))
        inter = next(a for a in b["artifacts"]
                     if a["kind"] == "sysml_interchange"
                     and "qn_registry" in a)
        assert len(inter["qn_registry"]) > 90

    def test_missing_file_404(self, env):
        with pytest.raises(FileNotFoundError):
            create_baseline(BaselineInput(
                title="x", sysml_files=["/nope/nope.sysml"]))


class TestImmutability:
    def test_identical_content_same_id(self, env):
        inp = BaselineInput(title="same", sysml_files=[_system_package()])
        b1 = create_baseline(inp)
        with pytest.raises(ValueError):   # same content -> same id
            create_baseline(BaselineInput(title="same",
                                          sysml_files=[_system_package()]))

    def test_content_change_new_id(self, env):
        b1 = create_baseline(BaselineInput(
            title="v1", sysml_files=[_system_package()]))
        src2 = "/tmp/changed.sysml"    # a MODIFIED copy changes the id
        with open(_system_package()) as fh:
            text = fh.read()
        with open(src2, "w") as fh:
            fh.write(text + "\n// rev2 comment\n")
        try:
            b2 = create_baseline(BaselineInput(
                title="v2", sysml_files=[src2]))
            assert b2["id"] != b1["id"]
        finally:
            os.unlink(src2)

    def test_derived_from_chain(self, env):
        b1 = create_baseline(BaselineInput(
            title="v1", sysml_files=[_system_package()]))
        b2 = create_baseline(BaselineInput(
            title="v2", sysml_files=[_system_package()],
            derived_from=b1["id"]))
        assert b2["derived_from"] == b1["id"]


class TestVerify:
    def test_verify_ok(self, env):
        b = create_baseline(BaselineInput(
            title="t", sysml_files=[_system_package()]))
        v = verify_baseline(b["id"])
        assert v["verified"] is True
        assert all(a["status"] == "ok" for a in v["artifacts"])

    def test_verify_detects_tampering(self, env, tmp_path):
        # tamper: store a DIFFERENT payload under the recorded digest's
        # slot by directly writing to an on-disk store
        root = str(tmp_path / "artifacts")
        set_artifact_store(ArtifactStore(root))
        b = create_baseline(BaselineInput(
            title="t", sysml_files=[_system_package()]))
        digest = next(a["sha256"] for a in b["artifacts"]
                      if a["kind"] == "sysml")
        with open(os.path.join(root, digest), "wb") as fh:
            fh.write(b"TAMPERED")   # same path, different bytes
        v = verify_baseline(b["id"])
        assert v["verified"] is False
        assert any(a["status"] == "MISSING" for a in v["artifacts"])


class TestEndpoints:
    def test_list_create_get(self, client, env):
        payload = {"title": "bl-1",
                   "sysml_files": [_system_package()],
                   "step_files": [NIST]}
        r = client.post("/oslc/step/baselines",
                        data=json.dumps(payload),
                        content_type="application/json")
        assert r.status_code == 201, r.data
        b = r.json
        assert b["id"].startswith("bl:")
        # list
        lst = client.get("/oslc/step/baselines")
        assert lst.json["count"] == 1
        # get with verify
        got = client.get(f"/oslc/step/baselines/{b['id']}?verify=1")
        assert got.status_code == 200
        assert got.json["integrity"]["verified"] is True

    def test_missing_title_400(self, client, env):
        r = client.post("/oslc/step/baselines",
                        data=json.dumps({"sysml_files": []}),
                        content_type="application/json")
        assert r.status_code == 400

    def test_unknown_404(self, client, env):
        r = client.get("/oslc/step/baselines/bl:nonexistent0000")
        assert r.status_code == 404

    def test_file_not_found_404(self, client, env):
        r = client.post("/oslc/step/baselines",
                        data=json.dumps({"title": "x",
                                         "sysml_files": ["/nope.sysml"]}),
                        content_type="application/json")
        assert r.status_code == 404


class TestVeeLinksSnapshot:
    def test_links_recorded_at_baseline_time(self, env, client):
        from app.api.adapter.namespaces.step.vee import (
            get_vee_registry, set_vee_registry, VeeRegistry,
        )
        set_vee_registry(VeeRegistry())
        try:
            get_vee_registry().link("P.Engine", "sysml:abc", "#4374",
                                    "4374")
            b = create_baseline(BaselineInput(
                title="with links", sysml_files=[_system_package()]))
            assert b["vee_links"], "link snapshot must ride the baseline"
            assert b["vee_links"][0]["sysml_qn"] == "P.Engine"
            # a SECOND baseline (same content) picks up the same links:
            with pytest.raises(ValueError):
                create_baseline(BaselineInput(
                    title="with links", sysml_files=[_system_package()]))
        finally:
            set_vee_registry(None)