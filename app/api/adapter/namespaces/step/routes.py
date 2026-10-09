# -*- coding: utf-8 -*-
"""flask-restx namespace wiring for the STEP domain."""

import os

from flask_restx import Resource, reqparse
from flask import request, make_response
from rdflib import Graph
from rdflib.plugin import PluginException

from app.api.adapter import api
from app.api.adapter.exceptions import NotModified
from app.api.adapter.namespaces.step.business import (
    get_step_resource,
    get_step_resource_list,
    create_step_product,
    create_step_product_definition,
    create_step_shape_representation,
    create_step_file,
    delete_step_resource,
)
from pyoslc.resources.domains.step import (
    StepFile, StepProduct, StepProductDefinition, StepShapeRepresentation,
)
from pyoslc.vocabularies.core import OSLC

STEP_TYPES = {
    StepProduct: ("product", "Product"),
    StepProductDefinition: ("product_definition", "ProductDefinition"),
    StepShapeRepresentation: ("shape_representation", "ShapeRepresentation"),
    StepFile: ("file", "StepFile"),
}


def _content_type():
    ct = request.headers.get("accept", "application/rdf+xml")
    if ct in ("application/json-ld", "application/json"):
        return "json-ld"
    return ct


def _serialize(graph):
    fmt = _content_type()
    data = graph.serialize(format=fmt)
    response = make_response(
        data.decode("utf-8") if not isinstance(data, str) else data, 200)
    response.headers["Content-Type"] = fmt
    response.headers["Oslc-Core-Version"] = "2.0"
    return response



def _list_get(resource_class):
    from app.api.adapter.namespaces.step.repository import get_step_repository as _g
    repo = _g()
    print("ROUTE-REPO id:", id(repo), "count:", len(repo.list()))
    try:
        elements = get_step_resource_list(request.base_url, "", "",
                                          resource_class=resource_class)
        graph = Graph()
        graph.bind("oslc", OSLC, override=False)
        for e in elements:
            e.to_rdf(graph, request.base_url)
        return _serialize(graph)
    except PluginException as pe:
        return {"status": "fail", "message": f"Content-Type Incompatible: {pe}"}, 400
    except Exception as e:
        return {"status": "fail", "message": f"An exception has occurred: {e}"}, 500


def _item_get(identifier):
    try:
        element = get_step_resource(request.base_url, identifier)
        if not element:
            from werkzeug.exceptions import NotFound
            raise NotFound()
        graph = Graph()
        element.to_rdf(graph, request.base_url)
        return _serialize(graph)
    except NotFound:
        raise  # proper 404 through flask-restx error handling
    except PluginException as pe:
        return {"status": "fail", "message": f"Content-Type Incompatible: {pe}"}, 400
    except Exception as e:
        return {"status": "fail", "message": f"An exception has occurred: {e}"}, 500


def _item_delete(identifier):
    result = delete_step_resource(identifier)
    if isinstance(result, NotModified):
        return make_response("{Not Modified}", 304)
    return make_response("{}", 200)


def _list_post(parser, create_func):
    content_type = request.headers.get("content-type", "application/rdf+xml")
    if "rdf+xml" in content_type:
        g = Graph()
        g.parse(data=request.data, format="xml")
        data = g
    elif "json" in content_type:
        data = request.get_json(force=True)
    else:
        data = parser.parse_args()
    result = create_func(data)
    if isinstance(result, NotModified):
        return {"status": "fail", "message": "Not Modified"}, 304
    if result is None:
        return {"status": "fail", "message": "Not Found"}, 400
    response = make_response("", 201)
    response.headers["Location"] = result.about
    return response


def _make_list_item_classes(list_cls_name, item_cls_name, label,
                            resource_class, create_func):
    list_cls = type(list_cls_name, (Resource,), {
        "get": lambda self: _list_get(resource_class),
        "post": lambda self: _list_post(_step_parser(), create_func),
    })
    item_cls = type(item_cls_name, (Resource,), {
        "get": lambda self, id: _item_get(id),
        "delete": lambda self, id: _item_delete(id),
    })
    return list_cls, item_cls


def _step_parser():
    p = reqparse.RequestParser()
    p.add_argument("identifier", type=str, required=True)
    p.add_argument("title", type=str, required=False)
    p.add_argument("description", type=str, required=False)
    p.add_argument("source_ref", type=str, required=False)
    p.add_argument("file_ref", type=str, required=False)
    return p


StepProductList, StepProductItem = _make_list_item_classes(
    "StepProductList", "StepProductItem", "product", StepProduct,
    create_step_product)
StepProductDefinitionList, StepProductDefinitionItem = _make_list_item_classes(
    "StepProductDefinitionList", "StepProductDefinitionItem",
    "product_definition", StepProductDefinition,
    create_step_product_definition)
StepShapeRepresentationList, StepShapeRepresentationItem = \
    _make_list_item_classes(
        "StepShapeRepresentationList", "StepShapeRepresentationItem",
        "shape_representation", StepShapeRepresentation,
        create_step_shape_representation)
StepFileList, StepFileItem = _make_list_item_classes(
    "StepFileList", "StepFileItem", "file", StepFile, create_step_file)


class StepFileDownload(Resource):
    """GET /oslc/step/file/<id>/model.stp — stream the raw Part 21 bytes
    so browser viewers can tessellate the model locally (occt-import-js
    in mvp-viewer). The file path is the resource's vocab#file value."""

    def get(self, id):
        from flask import send_file
        from app.api.adapter.namespaces.step.repository import (
            get_step_repository as _g,
        )
        res = _g().find(id)
        if res is None or not getattr(res, "file_ref", ""):
            return {"status": "fail", "message": "no backing file"}, 404
        path = res.file_ref
        if not os.path.exists(path):
            return {"status": "fail", "message": f"missing {path}"}, 404
        return send_file(path, mimetype="application/step",
                         as_attachment=False,
                         download_name=os.path.basename(path))