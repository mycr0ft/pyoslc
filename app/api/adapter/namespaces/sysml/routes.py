import logging

from flask import request, make_response
from flask_restx import Resource
from rdflib import Graph
from rdflib.plugin import PluginException

from app.api.adapter import api
from app.api.adapter.exceptions import NotModified
from app.api.adapter.namespaces.sysml.business import (
    create_sysml_element,
    create_sysml_relationship,
    create_sysml_package,
    create_sysml_definition,
    create_sysml_usage,
    create_sysml_item_definition,
    create_sysml_item_usage,
    create_sysml_part_definition,
    create_sysml_part_usage,
    create_sysml_port_definition,
    create_sysml_port_usage,
    create_sysml_requirement_definition,
    create_sysml_requirement_usage,
    create_sysml_concern_definition,
    create_sysml_concern_usage,
    create_sysml_action_definition,
    create_sysml_action_usage,
    create_sysml_state_definition,
    create_sysml_state_usage,
    create_sysml_constraint_definition,
    create_sysml_constraint_usage,
    create_sysml_view_definition,
    create_sysml_view_usage,
    create_sysml_viewpoint_definition,
    create_sysml_viewpoint_usage,
    create_sysml_feature,
    create_sysml_classifier,
    create_sysml_occurrence_definition,
    create_sysml_occurrence_usage,
    create_sysml_class,
    create_sysml_structure,
    create_sysml_data_type,
    create_sysml_behavior,
    create_sysml_function,
    create_sysml_predicate,
    create_sysml_library_package,
    create_sysml_attribute_definition,
    create_sysml_attribute_usage,
    create_sysml_enumeration_definition,
    create_sysml_enumeration_usage,
    create_sysml_calculation_definition,
    create_sysml_calculation_usage,
    create_sysml_case_definition,
    create_sysml_case_usage,
    create_sysml_use_case_definition,
    create_sysml_use_case_usage,
    create_sysml_analysis_case_definition,
    create_sysml_analysis_case_usage,
    create_sysml_verification_case_definition,
    create_sysml_verification_case_usage,
    create_sysml_connection_definition,
    create_sysml_connection_usage,
    create_sysml_flow_definition,
    create_sysml_flow_usage,
    create_sysml_interface_definition,
    create_sysml_interface_usage,
    create_sysml_allocation_definition,
    create_sysml_allocation_usage,
    create_sysml_rendering_definition,
    create_sysml_rendering_usage,
    create_sysml_reference_usage,
    create_sysml_conjugated_port_definition,
    create_sysml_connector_as_usage,
    create_sysml_succession_as_usage,
    create_sysml_binding_connector_as_usage,
    delete_sysml_element,
    get_sysml_element,
    get_sysml_element_list,
    get_sysml_relationship_list,
    update_sysml_element,
)
from app.api.adapter.namespaces.sysml.models import (
    sysml_element, sysml_relationship,
    sysml_package, sysml_definition, sysml_usage,
    sysml_item_definition, sysml_item_usage,
    sysml_part_definition, sysml_part_usage,
    sysml_port_definition, sysml_port_usage,
    sysml_requirement_definition, sysml_requirement_usage,
    sysml_concern_definition, sysml_concern_usage,
    sysml_action_definition, sysml_action_usage,
    sysml_state_definition, sysml_state_usage,
    sysml_constraint_definition, sysml_constraint_usage,
    sysml_view_definition, sysml_view_usage,
    sysml_viewpoint_definition, sysml_viewpoint_usage,
    sysml_feature, sysml_classifier,
    sysml_occurrence_definition, sysml_occurrence_usage,
    sysml_class, sysml_structure, sysml_data_type,
    sysml_behavior, sysml_function, sysml_predicate,
    sysml_library_package,
    sysml_attribute_definition, sysml_attribute_usage,
    sysml_enumeration_definition, sysml_enumeration_usage,
    sysml_calculation_definition, sysml_calculation_usage,
    sysml_case_definition, sysml_case_usage,
    sysml_use_case_definition, sysml_use_case_usage,
    sysml_analysis_case_definition, sysml_analysis_case_usage,
    sysml_verification_case_definition, sysml_verification_case_usage,
    sysml_connection_definition, sysml_connection_usage,
    sysml_flow_definition, sysml_flow_usage,
    sysml_interface_definition, sysml_interface_usage,
    sysml_allocation_definition, sysml_allocation_usage,
    sysml_rendering_definition, sysml_rendering_usage,
    sysml_reference_usage,
    sysml_conjugated_port_definition,
    sysml_connector_as_usage,
    sysml_succession_as_usage,
    sysml_binding_connector_as_usage,
)
from app.api.adapter.namespaces.sysml.parsers import (
    sysml_element_parser,
    sysml_relationship_parser,
    sysml_package_parser,
    sysml_definition_parser,
    sysml_usage_parser,
    sysml_item_definition_parser,
    sysml_item_usage_parser,
    sysml_part_definition_parser,
    sysml_part_usage_parser,
    sysml_port_definition_parser,
    sysml_port_usage_parser,
    sysml_requirement_definition_parser,
    sysml_requirement_usage_parser,
    sysml_concern_definition_parser,
    sysml_concern_usage_parser,
    sysml_action_definition_parser,
    sysml_action_usage_parser,
    sysml_state_definition_parser,
    sysml_state_usage_parser,
    sysml_constraint_definition_parser,
    sysml_constraint_usage_parser,
    sysml_view_definition_parser,
    sysml_view_usage_parser,
    sysml_viewpoint_definition_parser,
    sysml_viewpoint_usage_parser,
    sysml_feature_parser,
    sysml_classifier_parser,
    sysml_occurrence_definition_parser,
    sysml_occurrence_usage_parser,
    sysml_class_parser,
    sysml_structure_parser,
    sysml_data_type_parser,
    sysml_behavior_parser,
    sysml_function_parser,
    sysml_predicate_parser,
    sysml_library_package_parser,
    sysml_attribute_definition_parser,
    sysml_attribute_usage_parser,
    sysml_enumeration_definition_parser,
    sysml_enumeration_usage_parser,
    sysml_calculation_definition_parser,
    sysml_calculation_usage_parser,
    sysml_case_definition_parser,
    sysml_case_usage_parser,
    sysml_use_case_definition_parser,
    sysml_use_case_usage_parser,
    sysml_analysis_case_definition_parser,
    sysml_analysis_case_usage_parser,
    sysml_verification_case_definition_parser,
    sysml_verification_case_usage_parser,
    sysml_connection_definition_parser,
    sysml_connection_usage_parser,
    sysml_flow_definition_parser,
    sysml_flow_usage_parser,
    sysml_interface_definition_parser,
    sysml_interface_usage_parser,
    sysml_allocation_definition_parser,
    sysml_allocation_usage_parser,
    sysml_rendering_definition_parser,
    sysml_rendering_usage_parser,
    sysml_reference_usage_parser,
    sysml_conjugated_port_definition_parser,
    sysml_connector_as_usage_parser,
    sysml_succession_as_usage_parser,
    sysml_binding_connector_as_usage_parser,
)
from pyoslc.vocabularies.am import OSLC_AM
from pyoslc.vocabularies.core import OSLC
from pyoslc.vocabularies.sysml import OSLC_SYSML
from pyoslc.resources.domains.sysml import (
    SysMLElement, SysMLRelationship,
    SysMLPackage,
    SysMLDefinition, SysMLUsage,
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

logger = logging.getLogger(__name__)

_PATH_TYPE_MAP = {
    'element': SysMLElement,
    'relationship': SysMLRelationship,
    'package': SysMLPackage,
    'definition': SysMLDefinition,
    'usage': SysMLUsage,
    'itemDefinition': SysMLItemDefinition,
    'itemUsage': SysMLItemUsage,
    'partDefinition': SysMLPartDefinition,
    'partUsage': SysMLPartUsage,
    'portDefinition': SysMLPortDefinition,
    'portUsage': SysMLPortUsage,
    'requirementDefinition': SysMLRequirementDefinition,
    'requirementUsage': SysMLRequirementUsage,
    'concernDefinition': SysMLConcernDefinition,
    'concernUsage': SysMLConcernUsage,
    'actionDefinition': SysMLActionDefinition,
    'actionUsage': SysMLActionUsage,
    'stateDefinition': SysMLStateDefinition,
    'stateUsage': SysMLStateUsage,
    'constraintDefinition': SysMLConstraintDefinition,
    'constraintUsage': SysMLConstraintUsage,
    'viewDefinition': SysMLViewDefinition,
    'viewUsage': SysMLViewUsage,
    'viewpointDefinition': SysMLViewpointDefinition,
    'viewpointUsage': SysMLViewpointUsage,
    'feature': SysMLFeature,
    'classifier': SysMLClassifier,
    'occurrenceDefinition': SysMLOccurrenceDefinition,
    'occurrenceUsage': SysMLOccurrenceUsage,
    'class': SysMLClass,
    'structure': SysMLStructure,
    'dataType': SysMLDataType,
    'behavior': SysMLBehavior,
    'function': SysMLFunction,
    'predicate': SysMLPredicate,
    'libraryPackage': SysMLLibraryPackage,
    'attributeDefinition': SysMLAttributeDefinition,
    'attributeUsage': SysMLAttributeUsage,
    'enumerationDefinition': SysMLEnumerationDefinition,
    'enumerationUsage': SysMLEnumerationUsage,
    'calculationDefinition': SysMLCalculationDefinition,
    'calculationUsage': SysMLCalculationUsage,
    'caseDefinition': SysMLCaseDefinition,
    'caseUsage': SysMLCaseUsage,
    'useCaseDefinition': SysMLUseCaseDefinition,
    'useCaseUsage': SysMLUseCaseUsage,
    'analysisCaseDefinition': SysMLAnalysisCaseDefinition,
    'analysisCaseUsage': SysMLAnalysisCaseUsage,
    'verificationCaseDefinition': SysMLVerificationCaseDefinition,
    'verificationCaseUsage': SysMLVerificationCaseUsage,
    'connectionDefinition': SysMLConnectionDefinition,
    'connectionUsage': SysMLConnectionUsage,
    'flowDefinition': SysMLFlowDefinition,
    'flowUsage': SysMLFlowUsage,
    'interfaceDefinition': SysMLInterfaceDefinition,
    'interfaceUsage': SysMLInterfaceUsage,
    'allocationDefinition': SysMLAllocationDefinition,
    'allocationUsage': SysMLAllocationUsage,
    'renderingDefinition': SysMLRenderingDefinition,
    'renderingUsage': SysMLRenderingUsage,
    'referenceUsage': SysMLReferenceUsage,
    'conjugatedPortDefinition': SysMLConjugatedPortDefinition,
    'connectorAsUsage': SysMLConnectorAsUsage,
    'successionAsUsage': SysMLSuccessionAsUsage,
    'bindingConnectorAsUsage': SysMLBindingConnectorAsUsage,
}


def _resource_class_from_path():
    segment = request.path.rstrip('/').rsplit('/', 1)[-1]
    return _PATH_TYPE_MAP.get(segment)


class SysMLElementList(Resource):

    @api.response(200, 'The RDF formatted response of the SysML elements')
    def get(self):
        try:
            content_type = request.headers.get('accept', 'application/rdf+xml')
            if content_type in ('application/json-ld', 'application/json'):
                content_type = 'json-ld'

            elements = get_sysml_element_list(request.base_url, '', '', resource_class=SysMLElement)

            graph = Graph()
            graph.bind('oslc', OSLC, override=False)
            graph.bind('oslc_am', OSLC_AM, override=False)
            graph.bind('oslc_sysml', OSLC_SYSML, override=False)

            for element in elements:
                element.to_rdf(graph, request.base_url)

            data = graph.serialize(format=content_type)
            response = make_response(
                data.decode('utf-8') if not isinstance(data, str) else data, 200)
            response.headers['Content-Type'] = content_type
            response.headers['Oslc-Core-Version'] = "2.0"
            return response

        except PluginException as pe:
            return {'status': 'fail', 'message': f'Content-Type Incompatible: {pe}'}, 400
        except Exception as e:
            return {'status': 'fail', 'message': f'An exception has occurred: {e}'}, 500

    @api.expect(sysml_element)
    @api.response(201, 'SysML Element successfully created.')
    def post(self):
        content_type = request.headers['content-type']
        logger.debug('content-type: {}'.format(content_type))

        if content_type == 'application/rdf+xml':
            g = Graph()
            g.parse(data=request.data, format='xml')
            data = g
        else:
            data = sysml_element_parser.parse_args()

        result = create_sysml_element(data)

        if isinstance(result, NotModified):
            return {'status': 'fail', 'message': 'Not Modified'}, 304

        if result is None:
            return {'status': 'fail', 'message': 'Not Found'}, 400

        response = make_response('', 201)
        response.headers['Location'] = result.about
        return response


class SysMLElementItem(Resource):

    def get(self, id):
        try:
            content_type = request.headers.get('accept', 'application/rdf+xml')
            if content_type in ('application/json-ld', 'application/json'):
                content_type = 'json-ld'

            graph = Graph()
            element = get_sysml_element(request.base_url, id)
            if not element:
                return {'status': 'fail', 'message': 'Not Found'}, 404

            element.to_rdf(graph, request.base_url)

            data = graph.serialize(format=content_type)
            response = make_response(
                data.decode('utf-8') if not isinstance(data, str) else data, 200)
            response.headers['Content-Type'] = content_type
            response.headers['Oslc-Core-Version'] = "2.0"
            return response

        except PluginException as pe:
            return {'status': 'fail', 'message': f'Content-Type Incompatible: {pe}'}, 400
        except Exception as e:
            return {'status': 'fail', 'message': f'An exception has occurred: {e}'}, 500

    @api.expect(sysml_element)
    def put(self, id):
        data = sysml_element_parser.parse_args()
        if data:
            result = update_sysml_element(id, data)
            if isinstance(result, NotModified):
                return make_response('{Not Modified}', 304)
        return make_response('{}', 200)

    def delete(self, id):
        result = delete_sysml_element(id)
        if isinstance(result, NotModified):
            return make_response('{Not Modified}', 304)
        return make_response('{}', 200)


class SysMLRelationshipList(Resource):

    @api.response(200, 'The RDF formatted response of the SysML relationships')
    def get(self):
        try:
            content_type = request.headers.get('accept', 'application/rdf+xml')
            if content_type in ('application/json-ld', 'application/json'):
                content_type = 'json-ld'

            relationships = get_sysml_relationship_list(request.base_url, '', '')

            graph = Graph()
            graph.bind('oslc', OSLC, override=False)
            graph.bind('oslc_am', OSLC_AM, override=False)
            graph.bind('oslc_sysml', OSLC_SYSML, override=False)

            for rel in relationships:
                rel.to_rdf(graph, request.base_url)

            data = graph.serialize(format=content_type)
            response = make_response(
                data.decode('utf-8') if not isinstance(data, str) else data, 200)
            response.headers['Content-Type'] = content_type
            response.headers['Oslc-Core-Version'] = "2.0"
            return response

        except PluginException as pe:
            return {'status': 'fail', 'message': f'Content-Type Incompatible: {pe}'}, 400
        except Exception as e:
            return {'status': 'fail', 'message': f'An exception has occurred: {e}'}, 500

    @api.expect(sysml_relationship)
    @api.response(201, 'SysML Relationship successfully created.')
    def post(self):
        content_type = request.headers['content-type']

        if content_type == 'application/rdf+xml':
            g = Graph()
            g.parse(data=request.data, format='xml')
            data = g
        else:
            data = sysml_relationship_parser.parse_args()

        result = create_sysml_relationship(data)

        if isinstance(result, NotModified):
            return {'status': 'fail', 'message': 'Not Modified'}, 304

        if result is None:
            return {'status': 'fail', 'message': 'Not Found'}, 400

        response = make_response('', 201)
        response.headers['Location'] = result.about
        return response


class SysMLRelationshipItem(Resource):

    def get(self, id):
        try:
            content_type = request.headers.get('accept', 'application/rdf+xml')
            if content_type in ('application/json-ld', 'application/json'):
                content_type = 'json-ld'

            graph = Graph()
            element = get_sysml_element(request.base_url, id)
            if not element:
                return {'status': 'fail', 'message': 'Not Found'}, 404

            element.to_rdf(graph, request.base_url)

            data = graph.serialize(format=content_type)
            response = make_response(
                data.decode('utf-8') if not isinstance(data, str) else data, 200)
            response.headers['Content-Type'] = content_type
            response.headers['Oslc-Core-Version'] = "2.0"
            return response

        except PluginException as pe:
            return {'status': 'fail', 'message': f'Content-Type Incompatible: {pe}'}, 400
        except Exception as e:
            return {'status': 'fail', 'message': f'An exception has occurred: {e}'}, 500

    @api.expect(sysml_relationship)
    def put(self, id):
        data = sysml_relationship_parser.parse_args()
        if data:
            result = update_sysml_element(id, data)
            if isinstance(result, NotModified):
                return make_response('{Not Modified}', 304)
        return make_response('{}', 200)

    def delete(self, id):
        result = delete_sysml_element(id)
        if isinstance(result, NotModified):
            return make_response('{Not Modified}', 304)
        return make_response('{}', 200)


class SysMLPackageList(Resource):

    @api.response(200, 'The RDF formatted response of the SysML packages')
    def get(self):
        try:
            content_type = request.headers.get('accept', 'application/rdf+xml')
            if content_type in ('application/json-ld', 'application/json'):
                content_type = 'json-ld'

            elements = get_sysml_element_list(request.base_url, '', '', resource_class=SysMLPackage)

            graph = Graph()
            graph.bind('oslc', OSLC, override=False)
            graph.bind('oslc_am', OSLC_AM, override=False)
            graph.bind('oslc_sysml', OSLC_SYSML, override=False)

            for element in elements:
                element.to_rdf(graph, request.base_url)

            data = graph.serialize(format=content_type)
            response = make_response(
                data.decode('utf-8') if not isinstance(data, str) else data, 200)
            response.headers['Content-Type'] = content_type
            response.headers['Oslc-Core-Version'] = "2.0"
            return response

        except PluginException as pe:
            return {'status': 'fail', 'message': f'Content-Type Incompatible: {pe}'}, 400
        except Exception as e:
            return {'status': 'fail', 'message': f'An exception has occurred: {e}'}, 500

    @api.expect(sysml_package)
    @api.response(201, 'SysML Package successfully created.')
    def post(self):
        content_type = request.headers['content-type']

        if content_type == 'application/rdf+xml':
            g = Graph()
            g.parse(data=request.data, format='xml')
            data = g
        else:
            data = sysml_package_parser.parse_args()

        result = create_sysml_package(data)

        if isinstance(result, NotModified):
            return {'status': 'fail', 'message': 'Not Modified'}, 304

        if result is None:
            return {'status': 'fail', 'message': 'Not Found'}, 400

        response = make_response('', 201)
        response.headers['Location'] = result.about
        return response


class SysMLPackageItem(Resource):

    def get(self, id):
        try:
            content_type = request.headers.get('accept', 'application/rdf+xml')
            if content_type in ('application/json-ld', 'application/json'):
                content_type = 'json-ld'

            graph = Graph()
            element = get_sysml_element(request.base_url, id)
            if not element:
                return {'status': 'fail', 'message': 'Not Found'}, 404

            element.to_rdf(graph, request.base_url)

            data = graph.serialize(format=content_type)
            response = make_response(
                data.decode('utf-8') if not isinstance(data, str) else data, 200)
            response.headers['Content-Type'] = content_type
            response.headers['Oslc-Core-Version'] = "2.0"
            return response

        except PluginException as pe:
            return {'status': 'fail', 'message': f'Content-Type Incompatible: {pe}'}, 400
        except Exception as e:
            return {'status': 'fail', 'message': f'An exception has occurred: {e}'}, 500

    def delete(self, id):
        result = delete_sysml_element(id)
        if isinstance(result, NotModified):
            return make_response('{Not Modified}', 304)
        return make_response('{}', 200)


class SysMLDefinitionList(Resource):

    @api.response(200, 'The RDF formatted response of the SysML definitions')
    def get(self):
        try:
            content_type = request.headers.get('accept', 'application/rdf+xml')
            if content_type in ('application/json-ld', 'application/json'):
                content_type = 'json-ld'

            elements = get_sysml_element_list(request.base_url, '', '', resource_class=SysMLDefinition)

            graph = Graph()
            graph.bind('oslc', OSLC, override=False)
            graph.bind('oslc_am', OSLC_AM, override=False)
            graph.bind('oslc_sysml', OSLC_SYSML, override=False)

            for element in elements:
                element.to_rdf(graph, request.base_url)

            data = graph.serialize(format=content_type)
            response = make_response(
                data.decode('utf-8') if not isinstance(data, str) else data, 200)
            response.headers['Content-Type'] = content_type
            response.headers['Oslc-Core-Version'] = "2.0"
            return response

        except PluginException as pe:
            return {'status': 'fail', 'message': f'Content-Type Incompatible: {pe}'}, 400
        except Exception as e:
            return {'status': 'fail', 'message': f'An exception has occurred: {e}'}, 500

    @api.expect(sysml_definition)
    @api.response(201, 'SysML Definition successfully created.')
    def post(self):
        content_type = request.headers['content-type']

        if content_type == 'application/rdf+xml':
            g = Graph()
            g.parse(data=request.data, format='xml')
            data = g
        else:
            data = sysml_definition_parser.parse_args()

        result = create_sysml_definition(data)

        if isinstance(result, NotModified):
            return {'status': 'fail', 'message': 'Not Modified'}, 304

        if result is None:
            return {'status': 'fail', 'message': 'Not Found'}, 400

        response = make_response('', 201)
        response.headers['Location'] = result.about
        return response


class SysMLDefinitionItem(Resource):

    def get(self, id):
        try:
            content_type = request.headers.get('accept', 'application/rdf+xml')
            if content_type in ('application/json-ld', 'application/json'):
                content_type = 'json-ld'

            graph = Graph()
            element = get_sysml_element(request.base_url, id)
            if not element:
                return {'status': 'fail', 'message': 'Not Found'}, 404

            element.to_rdf(graph, request.base_url)

            data = graph.serialize(format=content_type)
            response = make_response(
                data.decode('utf-8') if not isinstance(data, str) else data, 200)
            response.headers['Content-Type'] = content_type
            response.headers['Oslc-Core-Version'] = "2.0"
            return response

        except PluginException as pe:
            return {'status': 'fail', 'message': f'Content-Type Incompatible: {pe}'}, 400
        except Exception as e:
            return {'status': 'fail', 'message': f'An exception has occurred: {e}'}, 500

    def delete(self, id):
        result = delete_sysml_element(id)
        if isinstance(result, NotModified):
            return make_response('{Not Modified}', 304)
        return make_response('{}', 200)


class SysMLUsageList(Resource):

    @api.response(200, 'The RDF formatted response of the SysML usages')
    def get(self):
        try:
            content_type = request.headers.get('accept', 'application/rdf+xml')
            if content_type in ('application/json-ld', 'application/json'):
                content_type = 'json-ld'

            elements = get_sysml_element_list(request.base_url, '', '', resource_class=SysMLUsage)

            graph = Graph()
            graph.bind('oslc', OSLC, override=False)
            graph.bind('oslc_am', OSLC_AM, override=False)
            graph.bind('oslc_sysml', OSLC_SYSML, override=False)

            for element in elements:
                element.to_rdf(graph, request.base_url)

            data = graph.serialize(format=content_type)
            response = make_response(
                data.decode('utf-8') if not isinstance(data, str) else data, 200)
            response.headers['Content-Type'] = content_type
            response.headers['Oslc-Core-Version'] = "2.0"
            return response

        except PluginException as pe:
            return {'status': 'fail', 'message': f'Content-Type Incompatible: {pe}'}, 400
        except Exception as e:
            return {'status': 'fail', 'message': f'An exception has occurred: {e}'}, 500

    @api.expect(sysml_usage)
    @api.response(201, 'SysML Usage successfully created.')
    def post(self):
        content_type = request.headers['content-type']

        if content_type == 'application/rdf+xml':
            g = Graph()
            g.parse(data=request.data, format='xml')
            data = g
        else:
            data = sysml_usage_parser.parse_args()

        result = create_sysml_usage(data)

        if isinstance(result, NotModified):
            return {'status': 'fail', 'message': 'Not Modified'}, 304

        if result is None:
            return {'status': 'fail', 'message': 'Not Found'}, 400

        response = make_response('', 201)
        response.headers['Location'] = result.about
        return response


class SysMLUsageItem(Resource):

    def get(self, id):
        try:
            content_type = request.headers.get('accept', 'application/rdf+xml')
            if content_type in ('application/json-ld', 'application/json'):
                content_type = 'json-ld'

            graph = Graph()
            element = get_sysml_element(request.base_url, id)
            if not element:
                return {'status': 'fail', 'message': 'Not Found'}, 404

            element.to_rdf(graph, request.base_url)

            data = graph.serialize(format=content_type)
            response = make_response(
                data.decode('utf-8') if not isinstance(data, str) else data, 200)
            response.headers['Content-Type'] = content_type
            response.headers['Oslc-Core-Version'] = "2.0"
            return response

        except PluginException as pe:
            return {'status': 'fail', 'message': f'Content-Type Incompatible: {pe}'}, 400
        except Exception as e:
            return {'status': 'fail', 'message': f'An exception has occurred: {e}'}, 500

    def delete(self, id):
        result = delete_sysml_element(id)
        if isinstance(result, NotModified):
            return make_response('{Not Modified}', 304)
        return make_response('{}', 200)


def _list_get(self):
    try:
        content_type = request.headers.get('accept', 'application/rdf+xml')
        if content_type in ('application/json-ld', 'application/json'):
            content_type = 'json-ld'

        resource_class = _resource_class_from_path()
        elements = get_sysml_element_list(request.base_url, '', '', resource_class=resource_class)

        graph = Graph()
        graph.bind('oslc', OSLC, override=False)
        graph.bind('oslc_am', OSLC_AM, override=False)
        graph.bind('oslc_sysml', OSLC_SYSML, override=False)

        for element in elements:
            element.to_rdf(graph, request.base_url)

        data = graph.serialize(format=content_type)
        response = make_response(
            data.decode('utf-8') if not isinstance(data, str) else data, 200)
        response.headers['Content-Type'] = content_type
        response.headers['Oslc-Core-Version'] = "2.0"
        return response

    except PluginException as pe:
        return {'status': 'fail', 'message': f'Content-Type Incompatible: {pe}'}, 400
    except Exception as e:
        return {'status': 'fail', 'message': f'An exception has occurred: {e}'}, 500


def _item_get(self, id):
    try:
        content_type = request.headers.get('accept', 'application/rdf+xml')
        if content_type in ('application/json-ld', 'application/json'):
            content_type = 'json-ld'

        graph = Graph()
        element = get_sysml_element(request.base_url, id)
        if not element:
            return {'status': 'fail', 'message': 'Not Found'}, 404

        element.to_rdf(graph, request.base_url)

        data = graph.serialize(format=content_type)
        response = make_response(
            data.decode('utf-8') if not isinstance(data, str) else data, 200)
        response.headers['Content-Type'] = content_type
        response.headers['Oslc-Core-Version'] = "2.0"
        return response

    except PluginException as pe:
        return {'status': 'fail', 'message': f'Content-Type Incompatible: {pe}'}, 400
    except Exception as e:
        return {'status': 'fail', 'message': f'An exception has occurred: {e}'}, 500


def _item_delete(self, id):
    result = delete_sysml_element(id)
    if isinstance(result, NotModified):
        return make_response('{Not Modified}', 304)
    return make_response('{}', 200)


def _list_post(self, parser, create_func):
    content_type = request.headers['content-type']

    if content_type == 'application/rdf+xml':
        g = Graph()
        g.parse(data=request.data, format='xml')
        data = g
    else:
        data = parser.parse_args()

    result = create_func(data)

    if isinstance(result, NotModified):
        return {'status': 'fail', 'message': 'Not Modified'}, 304

    if result is None:
        return {'status': 'fail', 'message': 'Not Found'}, 400

    response = make_response('', 201)
    response.headers['Location'] = result.about
    return response


class SysMLItemDefinitionList(Resource):

    @api.response(200, 'The RDF formatted response of SysML item definitions')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_item_definition)
    @api.response(201, 'SysML ItemDefinition successfully created.')
    def post(self):
        return _list_post(self, sysml_item_definition_parser,
                          create_sysml_item_definition)


class SysMLItemDefinitionItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLItemUsageList(Resource):

    @api.response(200, 'The RDF formatted response of SysML item usages')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_item_usage)
    @api.response(201, 'SysML ItemUsage successfully created.')
    def post(self):
        return _list_post(self, sysml_item_usage_parser,
                          create_sysml_item_usage)


class SysMLItemUsageItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLPartDefinitionList(Resource):

    @api.response(200, 'The RDF formatted response of SysML part definitions')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_part_definition)
    @api.response(201, 'SysML PartDefinition successfully created.')
    def post(self):
        return _list_post(self, sysml_part_definition_parser,
                          create_sysml_part_definition)


class SysMLPartDefinitionItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLPartUsageList(Resource):

    @api.response(200, 'The RDF formatted response of SysML part usages')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_part_usage)
    @api.response(201, 'SysML PartUsage successfully created.')
    def post(self):
        return _list_post(self, sysml_part_usage_parser,
                          create_sysml_part_usage)


class SysMLPartUsageItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLPortDefinitionList(Resource):

    @api.response(200, 'The RDF formatted response of SysML port definitions')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_port_definition)
    @api.response(201, 'SysML PortDefinition successfully created.')
    def post(self):
        return _list_post(self, sysml_port_definition_parser,
                          create_sysml_port_definition)


class SysMLPortDefinitionItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLPortUsageList(Resource):

    @api.response(200, 'The RDF formatted response of SysML port usages')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_port_usage)
    @api.response(201, 'SysML PortUsage successfully created.')
    def post(self):
        return _list_post(self, sysml_port_usage_parser,
                          create_sysml_port_usage)


class SysMLPortUsageItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLRequirementDefinitionList(Resource):

    @api.response(200, 'The RDF formatted response of SysML requirement definitions')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_requirement_definition)
    @api.response(201, 'SysML RequirementDefinition successfully created.')
    def post(self):
        return _list_post(self, sysml_requirement_definition_parser,
                          create_sysml_requirement_definition)


class SysMLRequirementDefinitionItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLRequirementUsageList(Resource):

    @api.response(200, 'The RDF formatted response of SysML requirement usages')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_requirement_usage)
    @api.response(201, 'SysML RequirementUsage successfully created.')
    def post(self):
        return _list_post(self, sysml_requirement_usage_parser,
                          create_sysml_requirement_usage)


class SysMLRequirementUsageItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLConcernDefinitionList(Resource):

    @api.response(200, 'The RDF formatted response of SysML concern definitions')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_concern_definition)
    @api.response(201, 'SysML ConcernDefinition successfully created.')
    def post(self):
        return _list_post(self, sysml_concern_definition_parser,
                          create_sysml_concern_definition)


class SysMLConcernDefinitionItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLConcernUsageList(Resource):

    @api.response(200, 'The RDF formatted response of SysML concern usages')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_concern_usage)
    @api.response(201, 'SysML ConcernUsage successfully created.')
    def post(self):
        return _list_post(self, sysml_concern_usage_parser,
                          create_sysml_concern_usage)


class SysMLConcernUsageItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLActionDefinitionList(Resource):

    @api.response(200, 'The RDF formatted response of SysML action definitions')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_action_definition)
    @api.response(201, 'SysML ActionDefinition successfully created.')
    def post(self):
        return _list_post(self, sysml_action_definition_parser,
                          create_sysml_action_definition)


class SysMLActionDefinitionItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLActionUsageList(Resource):

    @api.response(200, 'The RDF formatted response of SysML action usages')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_action_usage)
    @api.response(201, 'SysML ActionUsage successfully created.')
    def post(self):
        return _list_post(self, sysml_action_usage_parser,
                          create_sysml_action_usage)


class SysMLActionUsageItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLStateDefinitionList(Resource):

    @api.response(200, 'The RDF formatted response of SysML state definitions')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_state_definition)
    @api.response(201, 'SysML StateDefinition successfully created.')
    def post(self):
        return _list_post(self, sysml_state_definition_parser,
                          create_sysml_state_definition)


class SysMLStateDefinitionItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLStateUsageList(Resource):

    @api.response(200, 'The RDF formatted response of SysML state usages')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_state_usage)
    @api.response(201, 'SysML StateUsage successfully created.')
    def post(self):
        return _list_post(self, sysml_state_usage_parser,
                          create_sysml_state_usage)


class SysMLStateUsageItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLConstraintDefinitionList(Resource):

    @api.response(200, 'The RDF formatted response of SysML constraint definitions')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_constraint_definition)
    @api.response(201, 'SysML ConstraintDefinition successfully created.')
    def post(self):
        return _list_post(self, sysml_constraint_definition_parser,
                          create_sysml_constraint_definition)


class SysMLConstraintDefinitionItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLConstraintUsageList(Resource):

    @api.response(200, 'The RDF formatted response of SysML constraint usages')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_constraint_usage)
    @api.response(201, 'SysML ConstraintUsage successfully created.')
    def post(self):
        return _list_post(self, sysml_constraint_usage_parser,
                          create_sysml_constraint_usage)


class SysMLConstraintUsageItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLViewDefinitionList(Resource):

    @api.response(200, 'The RDF formatted response of SysML view definitions')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_view_definition)
    @api.response(201, 'SysML ViewDefinition successfully created.')
    def post(self):
        return _list_post(self, sysml_view_definition_parser,
                          create_sysml_view_definition)


class SysMLViewDefinitionItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLViewUsageList(Resource):

    @api.response(200, 'The RDF formatted response of SysML view usages')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_view_usage)
    @api.response(201, 'SysML ViewUsage successfully created.')
    def post(self):
        return _list_post(self, sysml_view_usage_parser,
                          create_sysml_view_usage)


class SysMLViewUsageItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLViewpointDefinitionList(Resource):

    @api.response(200, 'The RDF formatted response of SysML viewpoint definitions')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_viewpoint_definition)
    @api.response(201, 'SysML ViewpointDefinition successfully created.')
    def post(self):
        return _list_post(self, sysml_viewpoint_definition_parser,
                          create_sysml_viewpoint_definition)


class SysMLViewpointDefinitionItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLViewpointUsageList(Resource):

    @api.response(200, 'The RDF formatted response of SysML viewpoint usages')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_viewpoint_usage)
    @api.response(201, 'SysML ViewpointUsage successfully created.')
    def post(self):
        return _list_post(self, sysml_viewpoint_usage_parser,
                          create_sysml_viewpoint_usage)


class SysMLViewpointUsageItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


# --- Phase 8 route classes ---

class SysMLFeatureList(Resource):

    @api.response(200, 'The RDF formatted response of SysML features')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_feature)
    @api.response(201, 'SysML Feature successfully created.')
    def post(self):
        return _list_post(self, sysml_feature_parser, create_sysml_feature)


class SysMLFeatureItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLClassifierList(Resource):

    @api.response(200, 'The RDF formatted response of SysML classifiers')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_classifier)
    @api.response(201, 'SysML Classifier successfully created.')
    def post(self):
        return _list_post(self, sysml_classifier_parser, create_sysml_classifier)


class SysMLClassifierItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLOccurrenceDefinitionList(Resource):

    @api.response(200, 'The RDF formatted response of SysML occurrence definitions')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_occurrence_definition)
    @api.response(201, 'SysML OccurrenceDefinition successfully created.')
    def post(self):
        return _list_post(self, sysml_occurrence_definition_parser, create_sysml_occurrence_definition)


class SysMLOccurrenceDefinitionItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLOccurrenceUsageList(Resource):

    @api.response(200, 'The RDF formatted response of SysML occurrence usages')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_occurrence_usage)
    @api.response(201, 'SysML OccurrenceUsage successfully created.')
    def post(self):
        return _list_post(self, sysml_occurrence_usage_parser, create_sysml_occurrence_usage)


class SysMLOccurrenceUsageItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLClassList(Resource):

    @api.response(200, 'The RDF formatted response of SysML classes')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_class)
    @api.response(201, 'SysML Class successfully created.')
    def post(self):
        return _list_post(self, sysml_class_parser, create_sysml_class)


class SysMLClassItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLStructureList(Resource):

    @api.response(200, 'The RDF formatted response of SysML structures')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_structure)
    @api.response(201, 'SysML Structure successfully created.')
    def post(self):
        return _list_post(self, sysml_structure_parser, create_sysml_structure)


class SysMLStructureItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLDataTypeList(Resource):

    @api.response(200, 'The RDF formatted response of SysML data types')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_data_type)
    @api.response(201, 'SysML DataType successfully created.')
    def post(self):
        return _list_post(self, sysml_data_type_parser, create_sysml_data_type)


class SysMLDataTypeItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLBehaviorList(Resource):

    @api.response(200, 'The RDF formatted response of SysML behaviors')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_behavior)
    @api.response(201, 'SysML Behavior successfully created.')
    def post(self):
        return _list_post(self, sysml_behavior_parser, create_sysml_behavior)


class SysMLBehaviorItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLFunctionList(Resource):

    @api.response(200, 'The RDF formatted response of SysML functions')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_function)
    @api.response(201, 'SysML Function successfully created.')
    def post(self):
        return _list_post(self, sysml_function_parser, create_sysml_function)


class SysMLFunctionItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLPredicateList(Resource):

    @api.response(200, 'The RDF formatted response of SysML predicates')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_predicate)
    @api.response(201, 'SysML Predicate successfully created.')
    def post(self):
        return _list_post(self, sysml_predicate_parser, create_sysml_predicate)


class SysMLPredicateItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLLibraryPackageList(Resource):

    @api.response(200, 'The RDF formatted response of SysML library packages')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_library_package)
    @api.response(201, 'SysML LibraryPackage successfully created.')
    def post(self):
        return _list_post(self, sysml_library_package_parser, create_sysml_library_package)


class SysMLLibraryPackageItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLAttributeDefinitionList(Resource):

    @api.response(200, 'The RDF formatted response of SysML attribute definitions')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_attribute_definition)
    @api.response(201, 'SysML AttributeDefinition successfully created.')
    def post(self):
        return _list_post(self, sysml_attribute_definition_parser, create_sysml_attribute_definition)


class SysMLAttributeDefinitionItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLAttributeUsageList(Resource):

    @api.response(200, 'The RDF formatted response of SysML attribute usages')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_attribute_usage)
    @api.response(201, 'SysML AttributeUsage successfully created.')
    def post(self):
        return _list_post(self, sysml_attribute_usage_parser, create_sysml_attribute_usage)


class SysMLAttributeUsageItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLEnumerationDefinitionList(Resource):

    @api.response(200, 'The RDF formatted response of SysML enumeration definitions')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_enumeration_definition)
    @api.response(201, 'SysML EnumerationDefinition successfully created.')
    def post(self):
        return _list_post(self, sysml_enumeration_definition_parser, create_sysml_enumeration_definition)


class SysMLEnumerationDefinitionItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLEnumerationUsageList(Resource):

    @api.response(200, 'The RDF formatted response of SysML enumeration usages')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_enumeration_usage)
    @api.response(201, 'SysML EnumerationUsage successfully created.')
    def post(self):
        return _list_post(self, sysml_enumeration_usage_parser, create_sysml_enumeration_usage)


class SysMLEnumerationUsageItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLCalculationDefinitionList(Resource):

    @api.response(200, 'The RDF formatted response of SysML calculation definitions')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_calculation_definition)
    @api.response(201, 'SysML CalculationDefinition successfully created.')
    def post(self):
        return _list_post(self, sysml_calculation_definition_parser, create_sysml_calculation_definition)


class SysMLCalculationDefinitionItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLCalculationUsageList(Resource):

    @api.response(200, 'The RDF formatted response of SysML calculation usages')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_calculation_usage)
    @api.response(201, 'SysML CalculationUsage successfully created.')
    def post(self):
        return _list_post(self, sysml_calculation_usage_parser, create_sysml_calculation_usage)


class SysMLCalculationUsageItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLCaseDefinitionList(Resource):

    @api.response(200, 'The RDF formatted response of SysML case definitions')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_case_definition)
    @api.response(201, 'SysML CaseDefinition successfully created.')
    def post(self):
        return _list_post(self, sysml_case_definition_parser, create_sysml_case_definition)


class SysMLCaseDefinitionItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLCaseUsageList(Resource):

    @api.response(200, 'The RDF formatted response of SysML case usages')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_case_usage)
    @api.response(201, 'SysML CaseUsage successfully created.')
    def post(self):
        return _list_post(self, sysml_case_usage_parser, create_sysml_case_usage)


class SysMLCaseUsageItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLUseCaseDefinitionList(Resource):

    @api.response(200, 'The RDF formatted response of SysML use case definitions')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_use_case_definition)
    @api.response(201, 'SysML UseCaseDefinition successfully created.')
    def post(self):
        return _list_post(self, sysml_use_case_definition_parser, create_sysml_use_case_definition)


class SysMLUseCaseDefinitionItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLUseCaseUsageList(Resource):

    @api.response(200, 'The RDF formatted response of SysML use case usages')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_use_case_usage)
    @api.response(201, 'SysML UseCaseUsage successfully created.')
    def post(self):
        return _list_post(self, sysml_use_case_usage_parser, create_sysml_use_case_usage)


class SysMLUseCaseUsageItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLAnalysisCaseDefinitionList(Resource):

    @api.response(200, 'The RDF formatted response of SysML analysis case definitions')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_analysis_case_definition)
    @api.response(201, 'SysML AnalysisCaseDefinition successfully created.')
    def post(self):
        return _list_post(self, sysml_analysis_case_definition_parser, create_sysml_analysis_case_definition)


class SysMLAnalysisCaseDefinitionItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLAnalysisCaseUsageList(Resource):

    @api.response(200, 'The RDF formatted response of SysML analysis case usages')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_analysis_case_usage)
    @api.response(201, 'SysML AnalysisCaseUsage successfully created.')
    def post(self):
        return _list_post(self, sysml_analysis_case_usage_parser, create_sysml_analysis_case_usage)


class SysMLAnalysisCaseUsageItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLVerificationCaseDefinitionList(Resource):

    @api.response(200, 'The RDF formatted response of SysML verification case definitions')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_verification_case_definition)
    @api.response(201, 'SysML VerificationCaseDefinition successfully created.')
    def post(self):
        return _list_post(self, sysml_verification_case_definition_parser, create_sysml_verification_case_definition)


class SysMLVerificationCaseDefinitionItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLVerificationCaseUsageList(Resource):

    @api.response(200, 'The RDF formatted response of SysML verification case usages')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_verification_case_usage)
    @api.response(201, 'SysML VerificationCaseUsage successfully created.')
    def post(self):
        return _list_post(self, sysml_verification_case_usage_parser, create_sysml_verification_case_usage)


class SysMLVerificationCaseUsageItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLConnectionDefinitionList(Resource):

    @api.response(200, 'The RDF formatted response of SysML connection definitions')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_connection_definition)
    @api.response(201, 'SysML ConnectionDefinition successfully created.')
    def post(self):
        return _list_post(self, sysml_connection_definition_parser, create_sysml_connection_definition)


class SysMLConnectionDefinitionItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLConnectionUsageList(Resource):

    @api.response(200, 'The RDF formatted response of SysML connection usages')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_connection_usage)
    @api.response(201, 'SysML ConnectionUsage successfully created.')
    def post(self):
        return _list_post(self, sysml_connection_usage_parser, create_sysml_connection_usage)


class SysMLConnectionUsageItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLFlowDefinitionList(Resource):

    @api.response(200, 'The RDF formatted response of SysML flow definitions')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_flow_definition)
    @api.response(201, 'SysML FlowDefinition successfully created.')
    def post(self):
        return _list_post(self, sysml_flow_definition_parser, create_sysml_flow_definition)


class SysMLFlowDefinitionItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLFlowUsageList(Resource):

    @api.response(200, 'The RDF formatted response of SysML flow usages')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_flow_usage)
    @api.response(201, 'SysML FlowUsage successfully created.')
    def post(self):
        return _list_post(self, sysml_flow_usage_parser, create_sysml_flow_usage)


class SysMLFlowUsageItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLInterfaceDefinitionList(Resource):

    @api.response(200, 'The RDF formatted response of SysML interface definitions')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_interface_definition)
    @api.response(201, 'SysML InterfaceDefinition successfully created.')
    def post(self):
        return _list_post(self, sysml_interface_definition_parser, create_sysml_interface_definition)


class SysMLInterfaceDefinitionItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLInterfaceUsageList(Resource):

    @api.response(200, 'The RDF formatted response of SysML interface usages')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_interface_usage)
    @api.response(201, 'SysML InterfaceUsage successfully created.')
    def post(self):
        return _list_post(self, sysml_interface_usage_parser, create_sysml_interface_usage)


class SysMLInterfaceUsageItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLAllocationDefinitionList(Resource):

    @api.response(200, 'The RDF formatted response of SysML allocation definitions')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_allocation_definition)
    @api.response(201, 'SysML AllocationDefinition successfully created.')
    def post(self):
        return _list_post(self, sysml_allocation_definition_parser, create_sysml_allocation_definition)


class SysMLAllocationDefinitionItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLAllocationUsageList(Resource):

    @api.response(200, 'The RDF formatted response of SysML allocation usages')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_allocation_usage)
    @api.response(201, 'SysML AllocationUsage successfully created.')
    def post(self):
        return _list_post(self, sysml_allocation_usage_parser, create_sysml_allocation_usage)


class SysMLAllocationUsageItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLRenderingDefinitionList(Resource):

    @api.response(200, 'The RDF formatted response of SysML rendering definitions')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_rendering_definition)
    @api.response(201, 'SysML RenderingDefinition successfully created.')
    def post(self):
        return _list_post(self, sysml_rendering_definition_parser, create_sysml_rendering_definition)


class SysMLRenderingDefinitionItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLRenderingUsageList(Resource):

    @api.response(200, 'The RDF formatted response of SysML rendering usages')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_rendering_usage)
    @api.response(201, 'SysML RenderingUsage successfully created.')
    def post(self):
        return _list_post(self, sysml_rendering_usage_parser, create_sysml_rendering_usage)


class SysMLRenderingUsageItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLReferenceUsageList(Resource):

    @api.response(200, 'The RDF formatted response of SysML reference usages')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_reference_usage)
    @api.response(201, 'SysML ReferenceUsage successfully created.')
    def post(self):
        return _list_post(self, sysml_reference_usage_parser, create_sysml_reference_usage)


class SysMLReferenceUsageItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLConjugatedPortDefinitionList(Resource):

    @api.response(200, 'The RDF formatted response of SysML conjugated port definitions')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_conjugated_port_definition)
    @api.response(201, 'SysML ConjugatedPortDefinition successfully created.')
    def post(self):
        return _list_post(self, sysml_conjugated_port_definition_parser, create_sysml_conjugated_port_definition)


class SysMLConjugatedPortDefinitionItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLConnectorAsUsageList(Resource):

    @api.response(200, 'The RDF formatted response of SysML connector as usages')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_connector_as_usage)
    @api.response(201, 'SysML ConnectorAsUsage successfully created.')
    def post(self):
        return _list_post(self, sysml_connector_as_usage_parser, create_sysml_connector_as_usage)


class SysMLConnectorAsUsageItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLSuccessionAsUsageList(Resource):

    @api.response(200, 'The RDF formatted response of SysML succession as usages')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_succession_as_usage)
    @api.response(201, 'SysML SuccessionAsUsage successfully created.')
    def post(self):
        return _list_post(self, sysml_succession_as_usage_parser, create_sysml_succession_as_usage)


class SysMLSuccessionAsUsageItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)


class SysMLBindingConnectorAsUsageList(Resource):

    @api.response(200, 'The RDF formatted response of SysML binding connector as usages')
    def get(self):
        return _list_get(self)

    @api.expect(sysml_binding_connector_as_usage)
    @api.response(201, 'SysML BindingConnectorAsUsage successfully created.')
    def post(self):
        return _list_post(self, sysml_binding_connector_as_usage_parser, create_sysml_binding_connector_as_usage)


class SysMLBindingConnectorAsUsageItem(Resource):

    def get(self, id):
        return _item_get(self, id)

    def delete(self, id):
        return _item_delete(self, id)
