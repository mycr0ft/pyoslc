# -*- coding: utf-8 -*-
"""STEP namespace (P2): STEP AP242 product structure as OSLC resources.

Endpoints (under /oslc/step/...):
    GET  /product            list products
    POST /product            create (RDF/XML, JSON-LD, or JSON form)
    GET  /product/<id>       one product
    DELETE /product/<id>
    ... same for productDefinition, shapeRepresentation, file

The seeder (seeder.py) loads stepper's P1 output (JSON-LD) at startup.
"""

from flask_restx import Namespace

from app.api.adapter.namespaces.step.routes import (
    StepProductList, StepProductItem,
    StepProductDefinitionList, StepProductDefinitionItem,
    StepShapeRepresentationList, StepShapeRepresentationItem,
    StepFileList, StepFileItem,
)

step_ns = Namespace(name="step", description="STEP product structure",
                    path="/step")

step_ns.add_resource(StepProductList, "/product")
step_ns.add_resource(StepProductItem, "/product/<string:id>")
step_ns.add_resource(StepProductDefinitionList, "/productDefinition")
step_ns.add_resource(StepProductDefinitionItem,
                     "/productDefinition/<string:id>")
step_ns.add_resource(StepShapeRepresentationList, "/shapeRepresentation")
step_ns.add_resource(StepShapeRepresentationItem,
                     "/shapeRepresentation/<string:id>")
step_ns.add_resource(StepFileList, "/file")
step_ns.add_resource(StepFileItem, "/file/<string:id>")