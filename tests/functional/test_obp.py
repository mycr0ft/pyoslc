# -*- coding: utf-8 -*-
"""Phase C item 3 functional tests: the OBP domain + ISO/TS 10303-400
uuid relationship endpoints.

Full chain under test:
  .stp file
    -> stepper.bom.to_obp()  (the verified MIM → -3001 mapping)
       -> seed_from_step_file_obp()  → OBPResourceNode in OBPRouter
          -> GET /oslc/step/obp           (the OBP view, JSON)
          -> GET /oslc/step/obp/Part#4374 (one node)

  P3 vee links -> POST /oslc/step/uuid (sync)
     -> UuidRelationshipResource (-400 vocabulary: uuid_1/uuid_2/role)
        -> GET /oslc/step/uuid[/<identifier>]

  baselines: create_baseline() pins 'step_obp' as a third derived
  artifact kind (hash-pinned, verify-able like the others).
"""
import json
import os

import pytest

stepper = pytest.importorskip("stepper")

from app.api.adapter.namespaces.step.obp import (  # noqa: E402
    OBPRouter, get_obp_router, seed_from_step_file_obp,
    set_obp_router,
)
from app.api.adapter.namespaces.step.repository import (  # noqa: E402
    InMemoryStepRepository, set_step_repository,
)
from app.api.adapter.namespaces.step.vee import (  # noqa: E402
    VeeRegistry, get_vee_registry, set_vee_registry,
)
from pyoslc.resources.domains.obp import (  # noqa: E402
    OBPResourceNode, UuidRelationshipResource,
)

STEPPER_PROJECT = "/storage16/home/jfox/proj/stepper"
NIST = os.path.join(STEPPER_PROJECT, "tests", "fixtures", "nist",
                    "nist_ctc_01_asme1_ap242-e1.stp")


@pytest.fixture
def obp():
    set_obp_router(OBPRouter())
    yield get_obp_router()
    set_obp_router(None)


@pytest.fixture
def vee():
    set_vee_registry(VeeRegistry())
    yield get_vee_registry()
    set_vee_registry(None)


@pytest.fixture
def obp_seeded(obp):
    if os.path.exists(NIST):
        seed_from_step_file_obp(NIST)
    return obp


class TestOBPSeeder:
    def test_seed_creates_obp_nodes(self, obp_seeded):
        if not os.path.exists(NIST):
            pytest.skip("stepper fixtures not present")
        classes = {n.obp_class for n in obp_seeded.nodes()}
        assert "Part" in classes
        assert "PartVersion" in classes
        assert "IndividualPartView" in classes
        assert any(c.startswith("External") for c in classes)

    def test_seed_is_idempotent(self, obp_seeded):
        if not os.path.exists(NIST):
            pytest.skip("stepper fixtures not present")
        before = len(obp_seeded)
        seed_from_step_file_obp(NIST)
        assert len(obp_seeded) == before   # same keys overwritten, not duplicated

    def test_provenance_preserved(self, obp_seeded):
        if not os.path.exists(NIST):
            pytest.skip("stepper fixtures not present")
        parts = obp_seeded.nodes("Part")
        assert parts and parts[0].step_ref.startswith("#")

    def test_obp_refs_carried(self, obp_seeded):
        if not os.path.exists(NIST):
            pytest.skip("stepper fixtures not present")
        view = obp_seeded.nodes("IndividualPartView")[0]
        assert any(r.startswith("obp:PartVersion#") for r in view.obp_refs)
        assert any("GeometricModel" in r for r in view.obp_refs)


class TestOBPEndpoints:
    def test_obp_list_empty(self, client, obp):
        resp = client.get("/oslc/step/obp")
        assert resp.status_code == 200
        assert resp.json["count"] == 0

    def test_obp_list_seeded(self, client, obp_seeded):
        if not os.path.exists(NIST):
            pytest.skip("stepper fixtures not present")
        resp = client.get("/oslc/step/obp")
        assert resp.status_code == 200
        assert resp.json["count"] == len(obp_seeded)
        part = next(n for n in resp.json["obp_nodes"] if n["@type"] == "Part")
        assert part["step_ref"].startswith("#")

    def test_obp_class_filter(self, client, obp_seeded):
        if not os.path.exists(NIST):
            pytest.skip("stepper fixtures not present")
        resp = client.get("/oslc/step/obp?class=Part")
        assert resp.status_code == 200
        assert all(n["@type"] == "Part" for n in resp.json["obp_nodes"])
        assert resp.json["count"] >= 1

    def test_obp_item(self, client, obp_seeded):
        if not os.path.exists(NIST):
            pytest.skip("stepper fixtures not present")
        part = obp_seeded.nodes("Part")[0]
        resp = client.get(f"/oslc/step/obp/Part__{part.identifier}")
        assert resp.status_code == 200
        assert resp.json["@type"] == "Part"
        assert resp.json["step_ref"].startswith("#")

    def test_obp_item_404(self, client, obp):
        resp = client.get("/oslc/step/obp/Part__999999")
        assert resp.status_code == 404

    def test_obp_item_bad_key_400(self, client, obp):
        resp = client.get("/oslc/step/obp/WithoutSeparator")
        assert resp.status_code == 400


class TestUuidRelationships:
    def test_adapter_from_vee_link(self, vee):
        vee.link("P.Engine", "sysml:a1", "#4374", "4374")
        link = vee.all()[0]
        rel = UuidRelationshipResource.from_vee_link(link)
        assert rel.uuid_1 == "sysml:a1"
        assert rel.uuid_2 == "#4374"
        assert rel.role == "realizes"
        assert "sysml:a1" in rel.identifier and "4374" in rel.identifier
        assert "#" not in rel.identifier   # URL-safe (fragment would truncate)

    def test_uuid_sync_endpoint(self, client, vee, obp):
        vee.link("P.Engine", "sysml:a1", "#4374", "4374")
        resp = client.post("/oslc/step/uuid")
        assert resp.status_code == 201
        assert resp.json["converted"] == 1
        # idempotent second sync
        resp2 = client.post("/oslc/step/uuid")
        assert resp2.json["converted"] == 1
        assert resp2.json["total"] == 1

    def test_uuid_list_and_item(self, client, vee, obp):
        vee.link("P.Gearbox", "sysml:b2", "#11", "11", kind="specifies")
        client.post("/oslc/step/uuid")
        listing = client.get("/oslc/step/uuid")
        assert listing.json["count"] == 1
        row = listing.json["uuid_relationships"][0]
        assert row["role"] == "specifies"
        assert row["uuid_1"] == "sysml:b2" and row["uuid_2"] == "#11"
        # by identifier
        one = client.get(f"/oslc/step/uuid/{row['identifier']}")
        assert one.status_code == 200
        assert one.json["role"] == "specifies"

    def test_uuid_item_404(self, client, obp):
        resp = client.get("/oslc/step/uuid/nope")
        assert resp.status_code == 404

    def test_uuid_rdf_form(self, vee):
        """The -400 resource serializes to RDF in the uuid vocabulary."""
        vee.link("P.Engine", "sysml:a1", "#4374", "4374")
        rel = UuidRelationshipResource.from_vee_link(vee.all()[0])
        import rdflib
        g = rel.to_rdf(rdflib.Graph(), base_url="http://x/oslc/step/uuid/1")
        turtle = g.serialize(format="turtle")
        assert "ns1:UuidRelationship" in turtle
        # role is a RESOURCE (ns1:role <...#role/realizes>), not a literal
        assert "<https://github.com/mycr0ft/stepper/vocab/uuid#role/realizes>" in turtle
        assert "sysml:a1" in turtle


class TestBaselineOBPArtifact:
    def test_baseline_pins_step_obp(self, tmp_path, vee, obp):
        """create_baseline() adds the OBP payload as a third derived kind."""
        from app.api.adapter.namespaces.step.baselines import (
            BaselineInput, create_baseline, set_artifact_store,
        )
        from app.api.adapter.namespaces.step.baselines import (
            InMemoryArtifactStore, set_baseline_store, InMemoryBaselineStore,
        )
        if not os.path.exists(NIST):
            pytest.skip("stepper fixtures not present")
        set_artifact_store(InMemoryArtifactStore())
        set_baseline_store(InMemoryBaselineStore())
        try:
            b = create_baseline(BaselineInput(
                title="obp-baseline", step_files=[NIST]))
            kinds = [a["kind"] for a in b["artifacts"]]
            assert "step_obp" in kinds
            obp_art = next(a for a in b["artifacts"] if a["kind"] == "step_obp")
            assert obp_art["sha256"]
            # the pinned payload IS the obp json
            from app.api.adapter.namespaces.step.baselines import get_artifact_store
            blob = get_artifact_store().get(obp_art["sha256"])
            payload = json.loads(blob)
            assert payload["obm"] == "iso-ts-10303-3001"
            # verify pass covers the new artifact too
            from app.api.adapter.namespaces.step.baselines import verify_baseline
            v = verify_baseline(b["id"])
            assert v["verified"]
        finally:
            set_artifact_store(None)
            set_baseline_store(None)