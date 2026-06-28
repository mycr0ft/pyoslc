from rdflib import Graph, DCTERMS
from werkzeug.exceptions import NotFound

from app.api.adapter.exceptions import NotModified
from app.api.adapter.namespaces.sysml.repository import get_sysml_repository
from pyoslc.resources.domains.sysml import (
    SysMLElement, SysMLRelationship, SysMLNamespace,
    SysMLType, SysMLPackage, SysMLDefinition, SysMLUsage,
    SysMLItemDefinition, SysMLItemUsage,
    SysMLPartDefinition, SysMLPartUsage,
    SysMLPortDefinition, SysMLPortUsage,
    SysMLRequirementDefinition, SysMLRequirementUsage,
    SysMLConcernDefinition, SysMLConcernUsage,
    SysMLActionDefinition, SysMLActionUsage,
    SysMLStateDefinition, SysMLStateUsage,
    SysMLConstraintDefinition, SysMLConstraintUsage,
    SysMLViewDefinition, SysMLViewUsage,
    SysMLViewpointDefinition, SysMLViewpointUsage,
    SysMLFeature, SysMLClassifier,
    SysMLOccurrenceDefinition, SysMLOccurrenceUsage,
    SysMLClass, SysMLStructure, SysMLDataType,
    SysMLBehavior, SysMLFunction, SysMLPredicate,
    SysMLLibraryPackage,
    SysMLAttributeDefinition, SysMLAttributeUsage,
    SysMLEnumerationDefinition, SysMLEnumerationUsage,
    SysMLCalculationDefinition, SysMLCalculationUsage,
    SysMLCaseDefinition, SysMLCaseUsage,
    SysMLUseCaseDefinition, SysMLUseCaseUsage,
    SysMLAnalysisCaseDefinition, SysMLAnalysisCaseUsage,
    SysMLVerificationCaseDefinition, SysMLVerificationCaseUsage,
    SysMLConnectionDefinition, SysMLConnectionUsage,
    SysMLFlowDefinition, SysMLFlowUsage,
    SysMLInterfaceDefinition, SysMLInterfaceUsage,
    SysMLAllocationDefinition, SysMLAllocationUsage,
    SysMLRenderingDefinition, SysMLRenderingUsage,
    SysMLReferenceUsage,
    SysMLConjugatedPortDefinition,
    SysMLConnectorAsUsage,
    SysMLSuccessionAsUsage,
    SysMLBindingConnectorAsUsage,
)


def _repo():
    return get_sysml_repository()


def get_sysml_element(base_url, element_id):
    repo = _repo()
    element = repo.find(element_id)
    if element:
        about = base_url.replace('selector', 'element')
        element.about = about
    return element


def get_sysml_element_list(base_url, select, where, resource_class=None):
    repo = _repo()
    if resource_class is not None:
        return repo.list_by_type(resource_class)
    return repo.list()


def get_sysml_relationship_list(base_url, select, where):
    repo = _repo()
    return repo.list_relationships()


def _create_sysml_resource(resource_class, data):
    if data:
        resource = resource_class()
        if isinstance(data, Graph):
            resource.from_rdf(data)
            identifier = [(s, o) for s, o in data.subject_objects(DCTERMS.identifier)]
            if identifier:
                resource.identifier = identifier[0][1]
                resource.about = str(identifier[0][0])
        else:
            resource.from_json(data=data)

        repo = _repo()
        existing = repo.find(resource.identifier)
        if existing:
            return NotModified()

        repo.create(resource)
        return resource

    return NotFound()


def create_sysml_element(data):
    return _create_sysml_resource(SysMLElement, data)


def create_sysml_relationship(data):
    return _create_sysml_resource(SysMLRelationship, data)


def create_sysml_namespace(data):
    return _create_sysml_resource(SysMLNamespace, data)


def create_sysml_type(data):
    return _create_sysml_resource(SysMLType, data)


def create_sysml_package(data):
    return _create_sysml_resource(SysMLPackage, data)


def create_sysml_definition(data):
    return _create_sysml_resource(SysMLDefinition, data)


def create_sysml_usage(data):
    return _create_sysml_resource(SysMLUsage, data)


def create_sysml_item_definition(data):
    return _create_sysml_resource(SysMLItemDefinition, data)


def create_sysml_item_usage(data):
    return _create_sysml_resource(SysMLItemUsage, data)


def create_sysml_part_definition(data):
    return _create_sysml_resource(SysMLPartDefinition, data)


def create_sysml_part_usage(data):
    return _create_sysml_resource(SysMLPartUsage, data)


def create_sysml_port_definition(data):
    return _create_sysml_resource(SysMLPortDefinition, data)


def create_sysml_port_usage(data):
    return _create_sysml_resource(SysMLPortUsage, data)


def create_sysml_requirement_definition(data):
    return _create_sysml_resource(SysMLRequirementDefinition, data)


def create_sysml_requirement_usage(data):
    return _create_sysml_resource(SysMLRequirementUsage, data)


def create_sysml_concern_definition(data):
    return _create_sysml_resource(SysMLConcernDefinition, data)


def create_sysml_concern_usage(data):
    return _create_sysml_resource(SysMLConcernUsage, data)


def create_sysml_action_definition(data):
    return _create_sysml_resource(SysMLActionDefinition, data)


def create_sysml_action_usage(data):
    return _create_sysml_resource(SysMLActionUsage, data)


def create_sysml_state_definition(data):
    return _create_sysml_resource(SysMLStateDefinition, data)


def create_sysml_state_usage(data):
    return _create_sysml_resource(SysMLStateUsage, data)


def create_sysml_constraint_definition(data):
    return _create_sysml_resource(SysMLConstraintDefinition, data)


def create_sysml_constraint_usage(data):
    return _create_sysml_resource(SysMLConstraintUsage, data)


def create_sysml_view_definition(data):
    return _create_sysml_resource(SysMLViewDefinition, data)


def create_sysml_view_usage(data):
    return _create_sysml_resource(SysMLViewUsage, data)


def create_sysml_viewpoint_definition(data):
    return _create_sysml_resource(SysMLViewpointDefinition, data)


def create_sysml_viewpoint_usage(data):
    return _create_sysml_resource(SysMLViewpointUsage, data)


def update_sysml_element(element_id, data):
    if data:
        element = SysMLElement()
        if isinstance(data, Graph):
            element.from_rdf(data)
        else:
            element.from_json(data=data)

        repo = _repo()
        try:
            repo.update(str(element_id), element)
            return element
        except NotFound:
            raise NotModified()

    return NotFound()


def create_sysml_feature(data):
    return _create_sysml_resource(SysMLFeature, data)


def create_sysml_classifier(data):
    return _create_sysml_resource(SysMLClassifier, data)


def create_sysml_occurrence_definition(data):
    return _create_sysml_resource(SysMLOccurrenceDefinition, data)


def create_sysml_occurrence_usage(data):
    return _create_sysml_resource(SysMLOccurrenceUsage, data)


def create_sysml_class(data):
    return _create_sysml_resource(SysMLClass, data)


def create_sysml_structure(data):
    return _create_sysml_resource(SysMLStructure, data)


def create_sysml_data_type(data):
    return _create_sysml_resource(SysMLDataType, data)


def create_sysml_behavior(data):
    return _create_sysml_resource(SysMLBehavior, data)


def create_sysml_function(data):
    return _create_sysml_resource(SysMLFunction, data)


def create_sysml_predicate(data):
    return _create_sysml_resource(SysMLPredicate, data)


def create_sysml_library_package(data):
    return _create_sysml_resource(SysMLLibraryPackage, data)


def create_sysml_attribute_definition(data):
    return _create_sysml_resource(SysMLAttributeDefinition, data)


def create_sysml_attribute_usage(data):
    return _create_sysml_resource(SysMLAttributeUsage, data)


def create_sysml_enumeration_definition(data):
    return _create_sysml_resource(SysMLEnumerationDefinition, data)


def create_sysml_enumeration_usage(data):
    return _create_sysml_resource(SysMLEnumerationUsage, data)


def create_sysml_calculation_definition(data):
    return _create_sysml_resource(SysMLCalculationDefinition, data)


def create_sysml_calculation_usage(data):
    return _create_sysml_resource(SysMLCalculationUsage, data)


def create_sysml_case_definition(data):
    return _create_sysml_resource(SysMLCaseDefinition, data)


def create_sysml_case_usage(data):
    return _create_sysml_resource(SysMLCaseUsage, data)


def create_sysml_use_case_definition(data):
    return _create_sysml_resource(SysMLUseCaseDefinition, data)


def create_sysml_use_case_usage(data):
    return _create_sysml_resource(SysMLUseCaseUsage, data)


def create_sysml_analysis_case_definition(data):
    return _create_sysml_resource(SysMLAnalysisCaseDefinition, data)


def create_sysml_analysis_case_usage(data):
    return _create_sysml_resource(SysMLAnalysisCaseUsage, data)


def create_sysml_verification_case_definition(data):
    return _create_sysml_resource(SysMLVerificationCaseDefinition, data)


def create_sysml_verification_case_usage(data):
    return _create_sysml_resource(SysMLVerificationCaseUsage, data)


def create_sysml_connection_definition(data):
    return _create_sysml_resource(SysMLConnectionDefinition, data)


def create_sysml_connection_usage(data):
    return _create_sysml_resource(SysMLConnectionUsage, data)


def create_sysml_flow_definition(data):
    return _create_sysml_resource(SysMLFlowDefinition, data)


def create_sysml_flow_usage(data):
    return _create_sysml_resource(SysMLFlowUsage, data)


def create_sysml_interface_definition(data):
    return _create_sysml_resource(SysMLInterfaceDefinition, data)


def create_sysml_interface_usage(data):
    return _create_sysml_resource(SysMLInterfaceUsage, data)


def create_sysml_allocation_definition(data):
    return _create_sysml_resource(SysMLAllocationDefinition, data)


def create_sysml_allocation_usage(data):
    return _create_sysml_resource(SysMLAllocationUsage, data)


def create_sysml_rendering_definition(data):
    return _create_sysml_resource(SysMLRenderingDefinition, data)


def create_sysml_rendering_usage(data):
    return _create_sysml_resource(SysMLRenderingUsage, data)


def create_sysml_reference_usage(data):
    return _create_sysml_resource(SysMLReferenceUsage, data)


def create_sysml_conjugated_port_definition(data):
    return _create_sysml_resource(SysMLConjugatedPortDefinition, data)


def create_sysml_connector_as_usage(data):
    return _create_sysml_resource(SysMLConnectorAsUsage, data)


def create_sysml_succession_as_usage(data):
    return _create_sysml_resource(SysMLSuccessionAsUsage, data)


def create_sysml_binding_connector_as_usage(data):
    return _create_sysml_resource(SysMLBindingConnectorAsUsage, data)


def delete_sysml_element(element_id):
    repo = _repo()
    try:
        repo.delete(str(element_id))
        return True
    except NotFound:
        raise NotModified()
