import json
import logging
import os

from app.api.adapter.namespaces.sysml.repository import get_sysml_repository
from pyoslc.resources.domains.sysml import (
    SysMLElement,
    SysMLRelationship,
    SysMLNamespace,
    SysMLType,
    SysMLPackage,
    SysMLDefinition,
    SysMLUsage,
    SysMLItemDefinition,
    SysMLItemUsage,
    SysMLPartDefinition,
    SysMLPartUsage,
    SysMLPortDefinition,
    SysMLPortUsage,
    SysMLRequirementDefinition,
    SysMLRequirementUsage,
    SysMLAttributeDefinition,
    SysMLAttributeUsage,
    SysMLConnectionDefinition,
    SysMLConnectionUsage,
    SysMLInterfaceDefinition,
    SysMLInterfaceUsage,
    SysMLAllocationDefinition,
    SysMLAllocationUsage,
)

logger = logging.getLogger(__name__)

_TYPE_MAP = {
    'SysMLElement': SysMLElement,
    'SysMLRelationship': SysMLRelationship,
    'SysMLNamespace': SysMLNamespace,
    'SysMLType': SysMLType,
    'SysMLPackage': SysMLPackage,
    'SysMLDefinition': SysMLDefinition,
    'SysMLUsage': SysMLUsage,
    'SysMLItemDefinition': SysMLItemDefinition,
    'SysMLItemUsage': SysMLItemUsage,
    'SysMLPartDefinition': SysMLPartDefinition,
    'SysMLPartUsage': SysMLPartUsage,
    'SysMLPortDefinition': SysMLPortDefinition,
    'SysMLPortUsage': SysMLPortUsage,
    'SysMLRequirementDefinition': SysMLRequirementDefinition,
    'SysMLRequirementUsage': SysMLRequirementUsage,
    'SysMLAttributeDefinition': SysMLAttributeDefinition,
    'SysMLAttributeUsage': SysMLAttributeUsage,
    'SysMLConnectionDefinition': SysMLConnectionDefinition,
    'SysMLConnectionUsage': SysMLConnectionUsage,
    'SysMLInterfaceDefinition': SysMLInterfaceDefinition,
    'SysMLInterfaceUsage': SysMLInterfaceUsage,
    'SysMLAllocationDefinition': SysMLAllocationDefinition,
    'SysMLAllocationUsage': SysMLAllocationUsage,
}

_seeded = False


def seed_saturn_v(model_path=None):
    global _seeded
    if _seeded:
        return

    if model_path is None:
        base_dir = os.path.abspath(os.path.dirname(__file__))
        model_path = os.path.join(
            base_dir, '..', '..', '..', '..', '..',
            'examples', 'saturn_v', 'saturn_v.json'
        )
        model_path = os.path.normpath(model_path)

    if not os.path.exists(model_path):
        logger.warning('Saturn V model file not found at %s', model_path)
        return

    with open(model_path, 'r', encoding='utf-8') as f:
        elements = json.load(f)

    repo = get_sysml_repository()

    for entry in elements:
        type_name = entry.pop('type', None)
        if not type_name:
            logger.warning('Skipping element without type field: %s', entry.get('identifier'))
            continue

        resource_class = _TYPE_MAP.get(type_name)
        if not resource_class:
            logger.warning('Unknown SysML type %s, skipping', type_name)
            continue

        identifier = entry.get('identifier')
        if not identifier:
            logger.warning('Skipping element without identifier: %s', type_name)
            continue

        existing = repo.find(identifier)
        if existing:
            continue

        resource = resource_class()
        resource.from_json(entry)
        repo.create(resource)

    _seeded = True
    logger.info('Seeded %d SysML elements from Saturn V model', len(elements))
