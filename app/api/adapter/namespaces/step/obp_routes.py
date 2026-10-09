# -*- coding: utf-8 -*-
"""OBP REST routes (Phase C item 3).

    GET  /oslc/step/obp[?class=Part]        — all OBP nodes (JSON)
    GET  /oslc/step/obp/<Class>#<ref>       — one node
    GET  /oslc/step/uuid                    — all Uuid_relationship resources
    GET  /oslc/step/uuid/<identifier>
    POST /oslc/step/uuid                    — sync: P3 vee links → -400 form
"""
from flask import jsonify, request
from flask_restx import Resource

from app.api.adapter.namespaces.step.obp import (
    get_obp_router,
    seed_uuid_relationships_from_vee,
)


def _json_attr(v):
    """Attribute value → JSON-safe (refs keep a repr; lists expand)."""
    if isinstance(v, (list, tuple)):
        return [_json_attr(x) for x in v]
    if isinstance(v, dict):
        return {k: _json_attr(x) for k, x in v.items()}
    return str(v)


def _node_payload(node):
    return {
        "id": f"{node.obp_class}#{node.identifier}",
        "@type": node.obp_class,
        "title": node.title,
        "step_ref": node.step_ref,
        "attributes": {k: _json_attr(v) for k, v in node.attributes.items()},
        "obp_refs": node.obp_refs,
    }


class OBPNodeList(Resource):
    """GET /oslc/step/obp[?class=Part] — the OBP view of the seeded STEP data."""

    def get(self):
        router = get_obp_router()
        nodes = router.nodes(request.args.get("class"))
        return jsonify({
            "obp_nodes": [_node_payload(n) for n in nodes],
            "count": len(nodes),
        })


class OBPNodeItem(Resource):
    """GET /oslc/step/obp/<Class>__<identifier> — one OBP node.

    ('__' instead of '#' — a URL fragment cannot carry the key.)
    """

    def get(self, node_key: str):
        if "__" not in node_key:
            return {"status": "fail",
                    "message": "key must be <Class>__<identifier>"}, 400
        obp_class, identifier = node_key.split("__", 1)
        router = get_obp_router()
        node = router.find_node(obp_class, identifier)
        if node is None:
            return {"status": "fail",
                    "message": f"OBP node {node_key} not found"}, 404
        return jsonify(_node_payload(node))


class UuidRelationshipList(Resource):
    """GET /oslc/step/uuid — the -400 link form of the Vee registry."""

    def get(self):
        router = get_obp_router()
        rels = router.uuid_relationships()
        return jsonify({
            "uuid_relationships": [
                {
                    "identifier": rel.identifier,
                    "uuid_1": rel.uuid_1,
                    "uuid_2": rel.uuid_2,
                    "role": rel.role,
                }
                for rel in rels
            ],
            "count": len(rels),
        })

    def post(self):
        """POST /oslc/step/uuid — one-shot sync: P3 links → -400 form."""
        created = seed_uuid_relationships_from_vee()
        return jsonify({"status": "ok", "converted": len(created),
                        "total": len(get_obp_router().uuid_relationships())}), 201


class UuidRelationshipItem(Resource):
    """GET /oslc/step/uuid/<identifier>"""

    def get(self, identifier: str):
        router = get_obp_router()
        rel = router.find_uuid_relationship(identifier)
        if rel is None:
            return {"status": "fail",
                    "message": f"uuid relationship {identifier} not found"}, 404
        return jsonify({
            "identifier": rel.identifier,
            "uuid_1": rel.uuid_1,
            "uuid_2": rel.uuid_2,
            "role": rel.role,
        })


def register_obp_routes(step_ns):
    step_ns.add_resource(OBPNodeList, "/obp")
    step_ns.add_resource(OBPNodeItem, "/obp/<path:node_key>")
    step_ns.add_resource(UuidRelationshipList, "/uuid")
    step_ns.add_resource(UuidRelationshipItem, "/uuid/<path:identifier>")