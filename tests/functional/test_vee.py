# -*- coding: utf-8 -*-
"""P3 functional tests: the Vee-link registry.

Full chain under test:
  sysmlpy model
    -> to_interchange(stable_ids=True) -> qn_registry(document)
       -> POST /oslc/step/vee  (ingest mode, auto-match by leaf name)
          -> registry holds identity edges SysML-QN <-> STEP resource
             -> GET /oslc/step/vee returns the joined view
                -> manual link/unlink endpoints behave

Requires sysmlpy importable (the sibling repo; installed editable in
the dev venv like stepper). Skipped when absent.
"""

import json
import os

import pytest

sysmlpy = pytest.importorskip("sysmlpy")
from sysmlpy import loads, to_interchange, qn_registry  # noqa: E402

from app.api.adapter.namespaces.step.repository import (  # noqa: E402
    InMemoryStepRepository, set_step_repository,
)
from app.api.adapter.namespaces.step.seeder import seed_from_step_file  # noqa: E402
from app.api.adapter.namespaces.step.vee import (  # noqa: E402
    VeeRegistry, get_vee_registry, set_vee_registry,
)

STEPPER_PROJECT = "/storage16/home/jfox/proj/stepper"
NIST = os.path.join(STEPPER_PROJECT, "tests", "fixtures", "nist",
                    "nist_ctc_01_asme1_ap242-e1.stp")

MODEL = """
package NistModel {
    part def Product4374 {
        attribute thrust : ScalarValues::Real;
    }
}
"""


@pytest.fixture
def vee():
    set_vee_registry(VeeRegistry())
    yield get_vee_registry()
    set_vee_registry(None)


@pytest.fixture
def seeded_repo():
    set_step_repository(InMemoryStepRepository())
    if os.path.exists(NIST):
        seed_from_step_file(NIST)
    yield
    set_step_repository(None)


class TestVeeRegistryUnit:
    @staticmethod
    def _leaf(qn: str) -> str:
        return qn.rsplit(".", 1)[-1].strip("'\"").strip().lower()

    def test_link_dedupes_pairs(self, vee):
        vee.link("P.Engine", "sysml:a", "#1", "1")
        vee.link("P.Engine", "sysml:a", "#1", "1")   # same pair again
        assert len(vee.by_sysml("P.Engine")) == 1

    def test_kind_validation(self, vee):
        with pytest.raises(ValueError):
            vee.link("P.Engine", "sysml:a", "#1", "1", kind="bogus")

    def test_bidirectional_queries(self, vee):
        vee.link("P.Engine", "sysml:a", "#1", "1")
        vee.link("P.Gearbox", "sysml:b", "#1", "1")  # same STEP part
        assert len(vee.by_step("#1")) == 2
        assert len(vee.by_sysml("P.Engine")) == 1

    def test_unlink(self, vee):
        vee.link("P.Engine", "sysml:a", "#1", "1")
        assert vee.unlink("P.Engine", "#1")
        assert vee.all() == []

    def test_sidecar_round_trip(self, vee, tmp_path):
        vee.sidecar = str(tmp_path / "vee.json")
        vee.link("P.Engine", "sysml:a", "#1", "1")
        vee.save()
        vee2 = VeeRegistry(sidecar=str(tmp_path / "vee.json"))
        assert vee2.load() == 1
        assert len(vee2.all()) == 1
        assert vee2.by_sysml("P.Engine")[0].sysml_id == "sysml:a"


class TestQnRegistrySource:
    """The SysML side of the join (sysmlpy, via qn_registry)."""

    def test_registry_from_model(self):
        doc = to_interchange(loads(MODEL), stable_ids=True)
        reg = qn_registry(doc)
        assert "NistModel.Product4374" in reg
        assert reg["NistModel.Product4374"].startswith("sysml:")


class TestVeeEndpoints:
    def test_empty_get(self, client, vee):
        resp = client.get("/oslc/step/vee")
        assert resp.status_code == 200
        assert resp.json["count"] == 0

    def test_manual_link_post_and_get(self, client, vee):
        payload = {"sysml_qn": "P.Engine", "sysml_id": "sysml:abc",
                   "step_ref": "#4374", "step_resource_id": "4374"}
        resp = client.post("/oslc/step/vee", data=json.dumps(payload),
                           content_type="application/json")
        assert resp.status_code == 201
        assert resp.json["sysml_qn"] == "P.Engine"
        # query it back
        got = client.get("/oslc/step/vee?sysml_qn=P.Engine")
        assert got.json["count"] == 1
        # step_ref query (URL-escaped '#')
        got2 = client.get("/oslc/step/vee?step_ref=%234374")
        assert got2.json["count"] == 1

    def test_bad_kind_400(self, client, vee):
        payload = {"sysml_qn": "P.Engine", "sysml_id": "sysml:a",
                   "step_ref": "#1", "step_resource_id": "1",
                   "kind": "bogus"}
        resp = client.post("/oslc/step/vee", data=json.dumps(payload),
                           content_type="application/json")
        assert resp.status_code == 400

    def test_missing_fields_400(self, client, vee):
        resp = client.post("/oslc/step/vee", data=json.dumps({"sysml_qn": "x"}),
                           content_type="application/json")
        assert resp.status_code == 400
        assert "sysml_id" in resp.json["message"]

    def test_ingest_auto_links_by_leaf_name(self, client, vee,
                                            seeded_repo):
        """The full Vee chain: sysmlpy export -> registry -> auto-match
        against the seeded STEP resources by leaf name.   The NIST
        CTC-01 product's title is 'NIST Test Case 1' — the model's
        leaf-named part realizes it."""
        if not os.path.exists(NIST):
            pytest.skip("stepper fixtures not present")
        doc = to_interchange(loads(MODEL), stable_ids=True)
        qn_map = qn_registry(doc)
        resp = client.post("/oslc/step/vee", data=json.dumps({
            "registry": qn_map}), content_type="application/json")
        assert resp.status_code == 201, resp.json
        assert resp.json["status"] == "ok"
        # no name match between 'Product4374' and 'NIST Test Case 1'
        # — the auto-match reports zero new links (honest no-op)
        assert resp.json["new_links"] == 0

        # name-matching case: model leaf name EQUALS the product title
        # (SysML short names cannot contain spaces — use a quoted
        # short-name to mirror the STEP product's title)
        MODEL2 = MODEL.replace("Product4374", "'NIST Test Case 1'")
        doc2 = to_interchange(loads(MODEL2), stable_ids=True)
        resp2 = client.post("/oslc/step/vee", data=json.dumps({
            "registry": qn_registry(doc2)}), content_type="application/json")
        assert resp2.json["new_links"] == 1, resp2.json
        links = get_vee_registry().all()
        link = next(l for l in links if "NIST Test Case 1" in l.sysml_qn)
        assert link.sysml_id.startswith("sysml:")
        assert link.step_resource_id == "4374"