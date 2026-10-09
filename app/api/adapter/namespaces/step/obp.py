# -*- coding: utf-8 -*-
"""OBP domain repository + seeder (Phase C item 3).

The OBP repository mirrors the P2 step repository's lifecycle; the
seeder consumes stepper's ``to_obp``/``to_obp_json`` (the verified
MIM→-3001 mapping) and the Uuid_relationship adapter converts P3 Vee
links into ISO/TS 10303-400's link vocabulary.
"""

from __future__ import annotations

import logging
import os
from typing import Dict, List, Optional

from pyoslc.resources.domains.obp import (
    OBPResourceNode,
    UUID_VOCAB,
    UuidRelationshipResource,
)

logger = logging.getLogger(__name__)


# -- OBP repository (same ABC/lifecycle as the P2 step repository) ------------


class OBPRouter:
    """The OBP domain's in-memory registry. OBP nodes are KEYED by
    provenance (``<Class>#<step-ref>``) so re-seeding identical data is
    idempotent."""

    def __init__(self):
        self._nodes: Dict[str, OBPResourceNode] = {}
        self._uuid_rels: Dict[str, UuidRelationshipResource] = {}

    # -- OBP nodes ------------------------------------------------------
    def put(self, node: OBPResourceNode) -> OBPResourceNode:
        key = f"{node.obp_class}#{node.identifier}"
        self._nodes[key] = node
        return node

    def find_node(self, obp_class: str, identifier: str) -> Optional[OBPResourceNode]:
        return self._nodes.get(f"{obp_class}#{identifier}")

    def nodes(self, obp_class: Optional[str] = None) -> List[OBPResourceNode]:
        out = list(self._nodes.values())
        if obp_class:
            out = [n for n in out if n.obp_class == obp_class]
        return out

    def delete_node(self, obp_class: str, identifier: str) -> bool:
        key = f"{obp_class}#{identifier}"
        if key in self._nodes:
            del self._nodes[key]
            return True
        return False

    # -- uuid relationships (the -400 link form) -------------------------
    def put_uuid_relationship(self, rel: UuidRelationshipResource) -> UuidRelationshipResource:
        self._uuid_rels[rel.identifier] = rel
        return rel

    def uuid_relationships(self) -> List[UuidRelationshipResource]:
        return list(self._uuid_rels.values())

    def find_uuid_relationship(self, identifier: str) -> Optional[UuidRelationshipResource]:
        return self._uuid_rels.get(identifier)

    # -- lifecycle --------------------------------------------------------
    def clear(self):
        self._nodes.clear()
        self._uuid_rels.clear()

    def __len__(self):
        return len(self._nodes) + len(self._uuid_rels)


_router: Optional[OBPRouter] = None


def get_obp_router() -> OBPRouter:
    global _router
    if _router is None:
        _router = OBPRouter()
    return _router


def set_obp_router(router: Optional[OBPRouter]) -> None:
    global _router
    _router = router


# -- seeding ------------------------------------------------------------------


def seed_from_step_file_obp(stp_path: str) -> List[OBPResourceNode]:
    """Full pipe: .stp → stepper.bom.to_obp() → OBPResourceNode put.

    Idempotent: re-seeding the same file overwrites the same keys.
    """
    try:
        from stepper.bom import to_obp
    except ImportError as e:
        raise RuntimeError(
            "OBP seeding requires the stepper package (pip install stepper)") from e

    model = to_obp(stp_path, file_label=os.path.basename(stp_path))
    router = get_obp_router()
    created = []
    for oid, node in sorted(model.nodes.items()):
        res = OBPResourceNode.from_obp_node(node)
        router.put(res)
        created.append(res)
    logger.info("obp seeder: %d nodes from %s", len(created), stp_path)
    return created


def seed_uuid_relationships_from_vee() -> List[UuidRelationshipResource]:
    """Convert the P3 Vee registry into -400 Uuid_relationship resources."""
    from app.api.adapter.namespaces.step.vee import get_vee_registry

    router = get_obp_router()
    created = []
    for link in get_vee_registry().all():
        rel = UuidRelationshipResource.from_vee_link(link)
        router.put_uuid_relationship(rel)
        created.append(rel)
    logger.info("obp seeder: %d uuid relationships", len(created))
    return created