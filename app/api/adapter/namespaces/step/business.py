# -*- coding: utf-8 -*-
"""Business layer for the STEP domain (same shape as sysml/business.py)."""

from rdflib import Graph
from werkzeug.exceptions import NotFound

from app.api.adapter.exceptions import NotModified
from app.api.adapter.namespaces.step.repository import get_step_repository
from pyoslc.resources.domains.step import (
    StepFile, StepProduct, StepProductDefinition, StepShapeRepresentation,
)

_RESOURCE_CLASSES = {
    "product": StepProduct,
    "product_definition": StepProductDefinition,
    "shape_representation": StepShapeRepresentation,
    "file": StepFile,
}


def _repo():
    return get_step_repository()


def get_step_resource(base_url, identifier):
    repo = _repo()
    resource = repo.find(identifier)
    if resource:
        resource.about = base_url
    return resource


def get_step_resource_list(base_url, select, where, resource_class=None):
    repo = _repo()
    if resource_class is not None:
        return repo.list_by_type(resource_class)
    return repo.list()


def create_step_product(data):
    return _create_resource(StepProduct, data)


def create_step_product_definition(data):
    return _create_resource(StepProductDefinition, data)


def create_step_shape_representation(data):
    return _create_resource(StepShapeRepresentation, data)


def create_step_file(data):
    return _create_resource(StepFile, data)


def delete_step_resource(identifier):
    repo = _repo()
    try:
        repo.delete(identifier)
    except NotFound:
        return NotModified()
    return None


def _create_resource(resource_class, data):
    """Create from RDF graph or JSON dict (the sysml pattern)."""
    if not data:
        return None
    resource = resource_class()
    if isinstance(data, Graph):
        resource.from_rdf(data)
    elif isinstance(data, dict):
        _apply_json(resource, data)
    else:  # reqparse Namespace
        _apply_json(resource, {k: v for k, v in data.items()
                               if v is not None})
    repo = _repo()
    if repo.find(resource.identifier):
        return NotModified()
    repo.create(resource)
    return resource


def _apply_json(resource, data):
    for key, value in data.items():
        attr = key
        if key == "product" and hasattr(resource, "add_product"):
            resource.add_product(value)
            continue
        if key == "shape_representations" and hasattr(
                resource, "add_shape_representation"):
            resource.add_shape_representation(value)
            continue
        if key == "sysml_links" and hasattr(resource, "add_sysml_link"):
            resource.add_sysml_link(value)
            continue
        if hasattr(resource.__class__, attr) or attr in (
                "identifier", "title", "description", "source_ref",
                "file_ref", "product_id", "representation_kind",
                "geometry_item_count", "schema_name", "product_count",
                "check_verdict", "about"):
            try:
                setattr(resource, attr, value)
            except (AttributeError, TypeError, ValueError):
                pass