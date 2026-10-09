# -*- coding: utf-8 -*-
"""Seeder: load stepper's P1 structure output into the STEP repository.

Input shape is whatever ``stepper structure --format jsonld`` emits
(a ``@graph`` of products / product definitions / shape reps / the
file resource with ``stepper:*`` properties and ``sysml:part`` links).

Also accepted: stepper's Turtle output (parsed with rdflib first).

Usage from the app factory or a test fixture::

    from app.api.adapter.namespaces.step.seeder import seed_from_step_file
    seed_from_step_file("path/to/model.stp")   # requires stepper pkg
"""

import json
import logging
import os

from app.api.adapter.namespaces.step.repository import get_step_repository
from pyoslc.resources.domains.step import (
    StepFile, StepProduct, StepProductDefinition, StepShapeRepresentation,
)

logger = logging.getLogger(__name__)

STEP_VOCAB = "https://github.com/mycr0ft/stepper/vocab#"


def seed_from_jsonld(document, file_ref=None):
    """Seed the STEP repository from a P1 JSON-LD document (dict)."""
    repo = get_step_repository()
    created = []

    graph = document.get("@graph", []) if isinstance(document, dict) else []

    def _upsert(r):
        """Idempotent seeding — re-seeding the same file must not raise."""
        try:
            return repo.create(r)
        except ValueError:
            return repo.update(r.identifier, r) if repo.find(r.identifier) else r

    for res in graph:
        rid = res.get("@id", "")
        tail = rid.rstrip("/").rsplit("/", 1)[-1]
        if "/product/" in rid and "/product_definition/" not in rid:
            r = StepProduct(
                identifier=tail, title=res.get("dcterms:title", ""),
                description=res.get("dcterms:description", ""),
                source_ref=res.get("dcterms:identifier", ""))
            _upsert(r)
            created.append(r)
        elif "/product_definition/" in rid:
            r = StepProductDefinition(
                identifier=tail, title=res.get("dcterms:title", ""),
                source_ref=res.get("dcterms:identifier", ""))
            # sysml:part targets → shape representations (and the product)
            for part in res.get("sysml:part", []) or []:
                part_id = part.get("@id", "").rstrip("/").rsplit("/", 1)[-1]
                if "/shape_rep/" in part.get("@id", ""):
                    r.add_shape_representation(part["@id"])
                elif "/product/" in part.get("@id", ""):
                    r.add_product(part["@id"])
            _upsert(r)
            created.append(r)
        elif "/shape_rep/" in rid:
            r = StepShapeRepresentation(
                identifier=tail, title=res.get("dcterms:title", ""),
                source_ref=res.get("dcterms:identifier", ""),
                geometry_item_count=res.get("stepper:geometryItemCount", 0))
            # kind is in the title prefix ("KIND #ref")
            title = r.title or ""
            if " " in title and not r.representation_kind:
                r.representation_kind = title.split(" ")[0]
            _upsert(r)
            created.append(r)
        elif "/file/" in rid:
            r = StepFile(
                identifier=tail, title=res.get("dcterms:title", file_ref),
                description=res.get("dcterms:description", ""),
                schema_name=res.get("dcterms:description", ""),
                product_count=res.get("stepper:productCount", 0),
                file_ref=file_ref or res.get("dcterms:identifier", ""))
            _upsert(r)
            created.append(r)

    logger.info("step seeder: %d resources seeded", len(created))
    return created


def seed_from_turtle(turtle_text, file_ref=None):
    """Seed from stepper's Turtle output (parsed via rdflib)."""
    from rdflib import Graph, Namespace
    from rdflib.namespace import DCTERMS

    STEPPER = Namespace(STEP_VOCAB)
    g = Graph().parse(data=turtle_text, format="turtle")
    repo = get_step_repository()
    created = []

    for cls, kind_uri, builder in (
        (StepProduct, STEPPER.Product, lambda: StepProduct()),
        (StepProductDefinition, STEPPER.ProductDefinition,
         lambda: StepProductDefinition()),
        (StepShapeRepresentation, STEPPER.ShapeRepresentation,
         lambda: StepShapeRepresentation()),
        (StepFile, STEPPER.StepFile, lambda: StepFile()),
    ):
        for s in g.subjects(None, kind_uri):
            r = builder()
            r.about = str(s)
            r.identifier = next(
                (str(o) for o in g.objects(s, DCTERMS.identifier)),
                str(s).rstrip("/").rsplit("/", 1)[-1])
            r.title = next((str(o) for o in g.objects(s, DCTERMS.title)), "")
            for o in g.objects(s, STEPPER.sourceRef):
                r.source_ref = str(o)
            for o in g.objects(s, STEPPER.shapeRepresentation):
                r.add_shape_representation(str(o))
            for o in g.objects(s, STEPPER.product):
                r.add_product(str(o))
            for o in g.objects(s, STEPPER.geometryItemCount):
                r.geometry_item_count = int(o)
            for o in g.objects(s, STEPPER.schemaName):
                r.schema_name = str(o)
            for o in g.objects(s, STEPPER.productCount):
                r.product_count = int(o)
            _upsert(r)
            created.append(r)

    logger.info("step seeder: %d resources seeded (turtle)", len(created))
    return created


def seed_from_step_file(stp_path):
    """Full pipe: parse a .stp file with stepper and seed the repo.

    Requires the ``stepper`` package importable (its P1 emitter).
    """
    try:
        from stepper.structure import extract_structure, to_oslc_jsonld
    except ImportError as e:
        raise RuntimeError(
            "seeding from .stp requires the stepper package "
            "(pip install stepper)") from e

    s = extract_structure(stp_path, file_label=os.path.basename(stp_path))
    return seed_from_jsonld(to_oslc_jsonld(s), file_ref=stp_path)


def seed_app_models(app):
    """Flask startup hook: seed demo STEP models when the app config
    asks for it (STEP_FIXTURES env or config key — matches the sysml
    seeder convention)."""
    fixtures = app.config.get("STEP_FIXTURES")
    if not fixtures:
        fixtures = os.environ.get("STEP_FIXTURES")
    if not fixtures:
        return []
    created = []
    for path in fixtures.split(os.pathsep):
        if not path.strip():
            continue
        created.extend(seed_from_step_file(path.strip()))
    return created