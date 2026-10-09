# -*- coding: utf-8 -*-
"""STEP namespace (P2): STEP AP242 product structure as OSLC resources.

Endpoints (under /oslc/step/...):
    GET  /product            list products
    POST /product            create (RDF/XML, JSON-LD, or JSON form)
    GET  /product/<id>       one product
    DELETE /product/<id>
    ... same for productDefinition, shapeRepresentation, file
    GET/POST /vee            P3 Vee-link registry (identity edges)

The seeder (seeder.py) loads stepper's P1 output (JSON-LD) at startup.
"""

from flask import jsonify, request
from flask_restx import Namespace, Resource

from app.api.adapter.namespaces.step.routes import (
    StepProductList, StepProductItem,
    StepProductDefinitionList, StepProductDefinitionItem,
    StepShapeRepresentationList, StepShapeRepresentationItem,
    StepFileList, StepFileItem, StepFileDownload,
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
step_ns.add_resource(StepFileDownload, "/file/<string:id>/model.stp")

# -- P3: the Vee-link registry endpoint ------------------------------------

from flask import jsonify


class VeeLinkList(Resource):
    """GET /oslc/step/vee — all identity edges as JSON.

    Query params:
        ?sysml_qn=P.Engine   -> links for that SysML element
        ?step_ref=%234374    -> links for that STEP instance
    POST /oslc/step/vee — create one edge:
        {"sysml_qn": "P.Engine", "sysml_id": "sysml:…",
         "step_ref": "#4374", "step_resource_id": "4374",
         "kind": "realizes"}
    GET /oslc/step/vee/ingest?qn=<registry-json-url-or-inline>
        (POST) — auto-link via a sysmlpy qn_registry map:
        {"registry": {"P.Engine": "sysml:…"}, "match_by_leaf": true}
    """

    def get(self):
        from app.api.adapter.namespaces.step.vee import get_vee_registry
        reg = get_vee_registry()
        sysml_qn = request.args.get("sysml_qn")
        step_ref = request.args.get("step_ref")
        if sysml_qn:
            links = reg.by_sysml(sysml_qn)
        elif step_ref:
            links = reg.by_step(step_ref)
        else:
            links = reg.all()
        return jsonify({
            "vee_links": [l.to_dict() for l in links],
            "count": len(links),
        })

    def post(self):
        from app.api.adapter.namespaces.step.vee import get_vee_registry
        reg = get_vee_registry()
        data = request.get_json(force=True, silent=True) or {}
        if data.get("registry") is not None:
            # ingest mode: qn_registry map, auto-match by leaf name
            qn_map = data.get("registry") or {}
            try:
                new = reg.ingest_qn_registry(
                    qn_map, match_by_name=(lambda r: (r.title or "")
                                           .strip().lower())
                )
            except Exception as e:
                return {"status": "fail", "message": str(e)}, 400
            return jsonify({"status": "ok", "new_links": new,
                            "total": len(reg.all())}), 201
        required = ("sysml_qn", "sysml_id", "step_ref", "step_resource_id")
        missing = [k for k in required if not data.get(k)]
        if missing:
            return {"status": "fail",
                    "message": f"missing fields: {', '.join(missing)}"}, 400
        try:
            link = reg.link(data["sysml_qn"], data["sysml_id"],
                            data["step_ref"], data["step_resource_id"],
                            data.get("kind", "realizes"))
        except ValueError as e:
            return {"status": "fail", "message": str(e)}, 400
        return jsonify(link.to_dict()), 201


step_ns.add_resource(VeeLinkList, "/vee")

# -- P4: Config-Management baselines ---------------------------------------

from app.api.adapter.namespaces.step.baseline_routes import (
    BaselineList, BaselineItem,
)

step_ns.add_resource(BaselineList, "/baselines")
step_ns.add_resource(BaselineItem, "/baselines/<string:baseline_id>")

# -- Phase C item 3: the OBP domain + ISO/TS 10303-400 uuid links -------------

from app.api.adapter.namespaces.step.obp_routes import register_obp_routes

register_obp_routes(step_ns)