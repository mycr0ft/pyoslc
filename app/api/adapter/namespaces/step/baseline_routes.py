# -*- coding: utf-8 -*-
"""Baseline REST endpoints (P4): /oslc/step/baselines."""

import json

from flask import jsonify, request
from flask_restx import Resource


class BaselineList(Resource):
    """GET  /oslc/step/baselines           — all baselines (JSON)
    POST /oslc/step/baselines             — pin a new baseline:
        {"title": …, "sysml_files": […], "step_files": […],
         "description": …, "author": …, "derived_from": …}
    """

    def get(self):
        from app.api.adapter.namespaces.step.baselines import (
            get_baseline_store,
        )
        baselines = get_baseline_store().all()
        return jsonify({"baselines": baselines, "count": len(baselines)})

    def post(self):
        from app.api.adapter.namespaces.step.baselines import (
            BaselineInput, create_baseline,
        )
        data = request.get_json(force=True, silent=True) or {}
        title = (data.get("title") or "").strip()
        if not title:
            return {"status": "fail", "message": "title is required"}, 400
        sysml_files = data.get("sysml_files") or []
        step_files = data.get("step_files") or []
        if not sysml_files and not step_files:
            return {"status": "fail",
                    "message": "at least one sysml_files or step_files "
                               "entry is required"}, 400
        inp = BaselineInput(
            title=title,
            description=data.get("description", ""),
            sysml_files=list(sysml_files),
            step_files=list(step_files),
            derived_from=data.get("derived_from", ""),
            author=data.get("author", ""),
        )
        try:
            baseline = create_baseline(inp)
        except FileNotFoundError as e:
            return {"status": "fail", "message": str(e)}, 404
        except ValueError as e:
            return {"status": "fail", "message": str(e)}, 400
        except Exception as e:
            return {"status": "fail", "message": str(e)}, 500
        return jsonify(baseline), 201


class BaselineItem(Resource):
    """GET    /oslc/step/baselines/<id>   — one baseline
    DELETE   /oslc/step/baselines/<id>?verify=1 — verify integrity
             (DELETE is reserved; baselines are immutable — this
             endpoint only READS and VERIFIES)
    """

    def get(self, baseline_id):
        from app.api.adapter.namespaces.step.baselines import (
            get_baseline_store, verify_baseline,
        )
        baseline = get_baseline_store().find(baseline_id)
        if baseline is None:
            return {"status": "fail", "message": "Not Found"}, 404
        out = dict(baseline)
        if request.args.get("verify"):
            out["integrity"] = verify_baseline(baseline_id)
        return jsonify(out)