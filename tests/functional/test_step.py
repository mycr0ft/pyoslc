# -*- coding: utf-8 -*-
"""Functional tests for the P2 STEP domain adapter.

Chain under test (the P2 contract):
  stepper structure emitter (P1)
    -> seed_from_jsonld / seed_from_step_file
       -> InMemoryStepRepository
          -> REST endpoints /oslc/step/...
             -> rdflib-parsed OSLC responses

Provider: the catalog must advertise the Step-1 provider
(StepSpecification) alongside Project-1 and SysML-1.
"""

import json
import os

import pytest
from rdflib import Graph, Namespace, RDF
from rdflib.namespace import DCTERMS

from app.api.adapter.namespaces.step.repository import (
    InMemoryStepRepository, get_step_repository, set_step_repository,
)
from app.api.adapter.namespaces.step.seeder import (
    seed_from_jsonld, seed_from_step_file,
)
from pyoslc.resources.domains.step import (
    StepProduct, StepProductDefinition, StepShapeRepresentation, StepFile,
)

STEPPER = Namespace("https://github.com/mycr0ft/stepper/vocab#")

STEPPER_PROJECT = "/storage16/home/jfox/proj/stepper"
NIST_CTC01 = os.path.join(
    STEPPER_PROJECT, "tests", "fixtures", "nist",
    "nist_ctc_01_asme1_ap242-e1.stp")


def _nist_available():
    return os.path.exists(NIST_CTC01)


@pytest.fixture
def step_repo():
    set_step_repository(InMemoryStepRepository())
    yield get_step_repository()
    set_step_repository(None)


@pytest.fixture
def seeded(step_repo):
    return seed_from_step_file(os.path.normpath(NIST_CTC01))


class TestRepository:
    def test_create_and_find(self, step_repo):
        p = StepProduct(identifier="P1", title="Widget")
        step_repo.create(p)
        assert step_repo.find("P1") is p

    def test_type_filtering(self, step_repo):
        step_repo.create(StepProduct(identifier="P1", title="x"))
        step_repo.create(StepProductDefinition(identifier="D1", title="y"))
        assert len(step_repo.list_by_type(StepProduct)) == 1
        assert len(step_repo.list_by_type(StepProductDefinition)) == 1

    def test_duplicate_raises(self, step_repo):
        step_repo.create(StepProduct(identifier="P1"))
        with pytest.raises(ValueError):
            step_repo.create(StepProduct(identifier="P1"))


class TestSeeder:
    def test_seed_from_nist_file(self, seeded, step_repo):
        products = step_repo.list_by_type(StepProduct)
        pds = step_repo.list_by_type(StepProductDefinition)
        srs = step_repo.list_by_type(StepShapeRepresentation)
        assert len(products) == 1
        assert len(pds) >= 1
        assert len(srs) >= 1
        # product name flows from the P1 emitter
        assert any(p.title == "NIST Test Case 1" for p in products)

    def test_pd_links_shape_rep(self, seeded, step_repo):
        pds = step_repo.list_by_type(StepProductDefinition)
        linked = [pd for pd in pds if pd.shape_representations]
        assert linked, "at least one PD must link a shape representation"
        # the link is a resolvable repo id
        target = linked[0].shape_representations[0]
        assert target.rstrip("/").rsplit("/", 1)[-1] in {
            r.identifier for r in step_repo.list()}


class TestEndpoints:
    def test_product_list_jsonld(self, client, step_repo, seeded):
        resp = client.get(
            "/oslc/step/product",
            headers={"Accept": "application/json-ld"})
        assert resp.status_code == 200
        doc = json.loads(resp.data)
        # rdflib json-ld serialization emits a list of node objects
        assert doc, "JSON-LD body must be non-empty"
        nodes = doc if isinstance(doc, list) else [doc]
        assert any("step:Product" in str(n.get("@type", []))
                   or "stepper/vocab#Product" in str(n.get("@type", []))
                   for n in nodes), nodes

    def test_product_list_turtle(self, client, step_repo, seeded):
        resp = client.get("/oslc/step/product",
                          headers={"Accept": "text/turtle"})
        assert resp.status_code == 200
        g = Graph().parse(data=resp.data, format="turtle")
        types = list(g.subjects(RDF.type, STEPPER.Product))
        assert types, "at least one step:Product in the response"

    def test_product_item(self, client, step_repo, seeded):
        products = step_repo.list_by_type(StepProduct)
        pid = products[0].identifier
        resp = client.get(f"/oslc/step/product/{pid}",
                          headers={"Accept": "text/turtle"})
        assert resp.status_code == 200
        g = Graph().parse(data=resp.data, format="turtle")
        assert list(g.subjects(RDF.type, STEPPER.Product))

    def test_product_item_404(self, client, step_repo, seeded):
        resp = client.get("/oslc/step/product/nope",
                          headers={"Accept": "text/turtle"})
        assert resp.status_code == 404

    def test_shape_rep_item(self, client, step_repo, seeded):
        srs = step_repo.list_by_type(StepShapeRepresentation)
        sid = srs[0].identifier
        resp = client.get(f"/oslc/step/shapeRepresentation/{sid}",
                          headers={"Accept": "text/turtle"})
        assert resp.status_code == 200
        g = Graph().parse(data=resp.data, format="turtle")
        assert list(g.subjects(RDF.type, STEPPER.ShapeRepresentation))

    def test_creation_factory_json_post(self, client, step_repo, seeded):
        payload = {
            "identifier": "PROD-NEW",
            "title": "Created via factory",
            "source_ref": "#9999",
        }
        resp = client.post("/oslc/step/product",
                           data=json.dumps(payload),
                           content_type="application/json")
        # _list_post uses request.get_json for json content types
        assert resp.status_code == 201, resp.data
        assert step_repo.find("PROD-NEW") is not None


class TestCatalog:
    def test_catalog_advertises_step_provider(self, pyoslc, client,
                                              step_repo):
        resp = pyoslc.get_catalog("application/rdf+xml")
        assert resp.status_code == 200
        g = Graph().parse(data=resp.data, format="xml")
        # the Step-1 provider exists in the catalog
        names = list(g.objects(None,
                               DCTERMS.title))
        # loose check: provider titles include the STEP service provider
        assert any("STEP" in str(t) for t in names), \
            f"catalog lacks STEP provider; titles={[str(t) for t in names[:10]]}"