import logging
from datetime import datetime
from urllib.parse import urlparse
from xml.sax import SAXParseException

from flask import request, make_response, url_for, render_template
from flask_restx import Namespace
from rdflib import Graph
from rdflib.plugin import register
from rdflib.serializer import Serializer
import rdflib
from werkzeug.exceptions import UnsupportedMediaType, NotAcceptable, PreconditionFailed, NotFound, BadRequest
from werkzeug.http import http_date

from app.api.adapter import api
from app.api.adapter.namespaces.business import get_requirement_list, get_requirement, attributes, create_requirement, \
    update_requirement, delete_requirement
from app.api.adapter.resources.repository import get_requirement_repository
from app.api.adapter.namespaces.rm.parsers import specification_parser
from app.api.adapter.resources.resource_service import config_service_resource
from app.api.adapter.services.providers import ServiceProviderCatalogSingleton, RootServiceSingleton, PublisherSingleton
from app.api.adapter.services.specification import ServiceResource
from app.api.adapter.services.shapes import (
    build_requirement_shape, build_sysml_element_shape,
    build_sysml_relationship_shape, build_sysml_namespace_shape,
    build_sysml_type_shape, build_sysml_package_shape,
    build_sysml_definition_shape, build_sysml_usage_shape,
    build_sysml_item_definition_shape, build_sysml_item_usage_shape,
    build_sysml_part_definition_shape, build_sysml_part_usage_shape,
    build_sysml_port_definition_shape, build_sysml_port_usage_shape,
    build_sysml_requirement_definition_shape, build_sysml_requirement_usage_shape,
    build_sysml_concern_definition_shape, build_sysml_concern_usage_shape,
    build_sysml_action_definition_shape, build_sysml_action_usage_shape,
    build_sysml_state_definition_shape, build_sysml_state_usage_shape,
    build_sysml_constraint_definition_shape, build_sysml_constraint_usage_shape,
    build_sysml_view_definition_shape, build_sysml_view_usage_shape,
    build_sysml_viewpoint_definition_shape, build_sysml_viewpoint_usage_shape,
    build_sysml_feature_shape, build_sysml_classifier_shape,
    build_sysml_occurrence_definition_shape, build_sysml_occurrence_usage_shape,
    build_sysml_class_shape, build_sysml_structure_shape,
    build_sysml_data_type_shape, build_sysml_behavior_shape,
    build_sysml_function_shape, build_sysml_predicate_shape,
    build_sysml_library_package_shape,
    build_sysml_attribute_definition_shape, build_sysml_attribute_usage_shape,
    build_sysml_enumeration_definition_shape, build_sysml_enumeration_usage_shape,
    build_sysml_calculation_definition_shape, build_sysml_calculation_usage_shape,
    build_sysml_case_definition_shape, build_sysml_case_usage_shape,
    build_sysml_use_case_definition_shape, build_sysml_use_case_usage_shape,
    build_sysml_analysis_case_definition_shape, build_sysml_analysis_case_usage_shape,
    build_sysml_verification_case_definition_shape, build_sysml_verification_case_usage_shape,
    build_sysml_connection_definition_shape, build_sysml_connection_usage_shape,
    build_sysml_flow_definition_shape, build_sysml_flow_usage_shape,
    build_sysml_interface_definition_shape, build_sysml_interface_usage_shape,
    build_sysml_allocation_definition_shape, build_sysml_allocation_usage_shape,
    build_sysml_rendering_definition_shape, build_sysml_rendering_usage_shape,
    build_sysml_reference_usage_shape,
    build_sysml_conjugated_port_definition_shape,
    build_sysml_connector_as_usage_shape,
    build_sysml_succession_as_usage_shape,
    build_sysml_binding_connector_as_usage_shape,
)
from pyoslc.resources.domains.rm import Requirement
from pyoslc.resources.models import ResponseInfo, Compact, Preview
from pyoslc.rest.resource import OslcResource
from pyoslc.shacl.converter import oslc_shape_to_shacl, validate_resource

logger = logging.getLogger(__name__)

adapter_ns = Namespace(name='adapter', description='Python OSLC Adapter', path='/services',)

register(
    'rootservices-xml', Serializer,
    'pyoslc.serializers.jazzxml', 'JazzRootServiceSerializer'
)

config_service_resource(
    'specification', ServiceResource,
    'app.api.adapter.services.specification', 'Specification',
)

config_service_resource(
    'sysml_specification', ServiceResource,
    'app.api.adapter.services.specification', 'SysMLSpecification',
)


@adapter_ns.route('/catalog')
@api.representation('application/rdf+xml')
@api.representation('application/json-ld')
@api.representation('text/turtle')
class ServiceProviderCatalog(OslcResource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self):
        super().get()
        endpoint_url = url_for('{}.{}'.format(request.blueprint, self.endpoint))
        base_url = '{}{}'.format(request.url_root.rstrip('/'), endpoint_url)

        catalog_url = urlparse(base_url).geturl()

        catalog = ServiceProviderCatalogSingleton.get_catalog(catalog_url)
        catalog.to_rdf(self.graph)

        response = self.create_response(graph=self.graph)
        response.headers['Link'] = '<http://www.w3.org/ns/ldp#BasicContainer>; rel="type"'
        return response

    def options(self):
        response = make_response('', 204)
        response.headers['Allow'] = 'GET,OPTIONS,HEAD'
        oslc_version = OslcResource.get_requested_version()
        response.headers['OSLC-Core-Version'] = oslc_version
        return response


@adapter_ns.route('/provider/<service_provider_id>')
@api.representation('application/rdf+xml')
@api.representation('application/json-ld')
@api.representation('text/turtle')
class ServiceProvider(OslcResource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def get(self, service_provider_id):
        super().get()
        endpoint_url = url_for('{}.{}'.format(request.blueprint, self.endpoint),
                               service_provider_id=service_provider_id)
        base_url = '{}{}'.format(request.url_root.rstrip('/'), endpoint_url)

        service_provider_url = urlparse(base_url).geturl()

        provider = ServiceProviderCatalogSingleton.get_provider(service_provider_url, service_provider_id)

        if not provider:
            return OslcResource.build_error_response(
                404, 'No resources with ID {}'.format(service_provider_id))

        provider.to_rdf(self.graph)
        response = self.create_response(graph=self.graph)
        response.headers['Link'] = '<http://www.w3.org/ns/ldp#BasicContainer>; rel="type"'
        return response

    def options(self, service_provider_id):
        response = make_response('', 204)
        response.headers['Allow'] = 'GET,OPTIONS,HEAD'
        oslc_version = OslcResource.get_requested_version()
        response.headers['OSLC-Core-Version'] = oslc_version
        return response


@adapter_ns.route('/provider/<service_provider_id>/resources/requirement')
@api.representation('application/rdf+xml')
@api.representation('application/json-ld')
@api.representation('text/turtle')
class ResourceOperation(OslcResource):

    def get(self, service_provider_id):
        super().get()

        select = request.args.get('oslc.select', '')
        where = request.args.get('oslc.where', '')

        endpoint_url = url_for('{}.{}'.format(request.blueprint, self.endpoint),
                               service_provider_id=service_provider_id)
        base_url = '{}{}'.format(request.url_root.rstrip('/'), endpoint_url)

        data = get_requirement_list(base_url, select, where)
        if len(data) == 0:
            return OslcResource.build_error_response(
                404, 'No resources from provider with ID {}'.format(service_provider_id))

        services_base = base_url.split('/provider/')[0]
        requirement_shape = services_base + '/resourceShapes/requirement'
        for req in data:
            req.instance_shape = requirement_shape

        response_info = ResponseInfo(base_url)
        response_info.total_count = len(data)
        response_info.title = 'Query Results for Requirements'

        response_info.members = data
        response_info.to_rdf(self.graph)

        response = self.create_response(graph=self.graph)
        response.headers['Link'] = '<http://www.w3.org/ns/ldp#BasicContainer>; rel="type"'
        return response

    def options(self, service_provider_id):
        response = make_response('', 204)
        response.headers['Allow'] = 'POST,GET,OPTIONS,HEAD,PUT'
        response.headers['Accept-Post'] = 'text/turtle, application/ld+json'
        oslc_version = OslcResource.get_requested_version()
        response.headers['OSLC-Core-Version'] = oslc_version
        return response

    # @adapter_ns.expect(specification)
    def post(self, service_provider_id):
        accept = request.headers.get('accept')
        if not (accept in ('application/rdf+xml', 'application/json', 'application/ld+json',
                           'application/xml', 'application/atom+xml')):
            raise UnsupportedMediaType

        endpoint_url = url_for('{}.{}'.format(request.blueprint, self.endpoint),
                               service_provider_id=service_provider_id)
        base_url = '{}{}'.format(request.url_root.rstrip('/'), endpoint_url)

        if accept == 'application/json':
            data = specification_parser.parse_args()
        else:
            try:
                data = Graph().parse(data=request.data, format='xml')
            except SAXParseException:
                raise BadRequest()

        req = create_requirement(data)
        if isinstance(req, Requirement):
            req.to_rdf(self.graph, base_url=base_url, attributes=attributes)
            data = self.graph.serialize(format='pretty-xml')

            # Sending the response to the client
            response = make_response(data.decode('utf-8') if not isinstance(data, str) else data, 201)
            response.headers['Content-Type'] = 'application/rdf+xml; charset=UTF-8'
            response.headers['OSLC-Core-Version'] = OslcResource.get_requested_version()
            response.headers['Location'] = base_url + '/' + req.identifier
            response.set_etag(req.digestion())
            response.headers['Last-Modified'] = http_date(datetime.now())

            return response
        else:
            return OslcResource.build_error_response(req.code, req.description)


@adapter_ns.route('/provider/<service_provider_id>/resources/requirement/<requirement_id>')
@api.representation('application/rdf+xml')
@api.representation('application/json-ld')
@api.representation('text/turtle')
class ResourcePreview(OslcResource):

    def get(self, service_provider_id, requirement_id):
        super().get()

        accept = request.headers['accept']

        endpoint_url = url_for('{}.{}'.format(request.blueprint, self.endpoint),
                               service_provider_id=service_provider_id, requirement_id=requirement_id)
        base_url = '{}{}'.format(request.url_root.rstrip('/'), endpoint_url)

        requirement = get_requirement(base_url, requirement_id)
        if requirement:
            requirement.about = base_url
            services_base = base_url.split('/provider/')[0]
            requirement.instance_shape = services_base + '/resourceShapes/requirement'
            requirement.to_rdf(self.graph, base_url, attributes)

        if 'application/x-oslc-compact+xml' in accept or ', application/x-jazz-compact-rendering' in accept:
            compact = Compact(about=base_url)
            compact.title = requirement.identifier if requirement else 'REQ Not Found'
            compact.icon = url_for('oslc.static', filename='pyicon24.ico', _external=True)

            small_preview = Preview()
            small_preview.document = base_url + '/smallPreview'
            small_preview.hint_width = '45em'
            small_preview.hint_height = '10em'

            large_preview = Preview()
            large_preview.document = base_url + '/largePreview'
            large_preview.hint_width = '45em'
            large_preview.hint_height = '20em'

            compact.small_preview = small_preview
            compact.large_preview = large_preview

            compact.to_rdf(self.graph)

        response = self.create_response(graph=self.graph,
                                        accept='application/x-oslc-compact+xml',
                                        rdf_format='pretty-xml',
                                        etag=True)
        response.headers['Link'] = '<http://www.w3.org/ns/ldp#Resource>; rel="type"'
        return response

    def put(self, service_provider_id, requirement_id):
        accept = request.headers.get('accept')
        if not (accept in ('application/rdf+xml', 'application/json', 'application/ld+json',
                           'application/xml', 'application/atom+xml')):
            raise UnsupportedMediaType

        content = request.headers.get('content-type')
        if not (content in ('application/rdf+xml', 'application/json', 'application/ld+json',
                            'application/xml', 'application/atom+xml')):
            raise UnsupportedMediaType

        endpoint_url = url_for('{}.{}'.format(request.blueprint, self.endpoint),
                               service_provider_id=service_provider_id, requirement_id=requirement_id)
        base_url = '{}{}'.format(request.url_root.rstrip('/'), endpoint_url)

        etag = request.headers.get(key='If-Match', default=None, type=str)

        repo = get_requirement_repository()
        r = repo.find(requirement_id)
        r.about = base_url

        if not r:
            raise NotFound()
        # elif r.identifier != requirement_id:
        #     raise Conflict()
        elif not etag:
            raise BadRequest()
        else:
            dig = r.digestion()
            if dig != etag.strip("\""):
                raise PreconditionFailed()

        g = Graph()
        try:
            data = g.parse(data=request.data, format='xml')
        except SAXParseException:
            raise NotAcceptable()

        req = update_requirement(requirement_id, data)
        if isinstance(req, Requirement):
            req.to_rdf(self.graph, base_url, attributes)
            return self.create_response(self.graph)
        else:
            return OslcResource.build_error_response(req.code, req.description)

    def delete(self, service_provider_id, requirement_id):
        repo = get_requirement_repository()
        r = repo.find(requirement_id)

        if r:
            req = delete_requirement(requirement_id)
            if req:
                response = make_response('Resource deleted.', 200)
                return response
            else:
                return OslcResource.build_error_response(req.code, req.description)
        else:
            return OslcResource.build_error_response(404, 'The resource was not found.')

    def options(self, service_provider_id, requirement_id):
        response = make_response('', 204)
        response.headers['Allow'] = 'GET,PUT,DELETE,OPTIONS,HEAD'
        oslc_version = OslcResource.get_requested_version()
        response.headers['OSLC-Core-Version'] = oslc_version
        return response


@adapter_ns.route('/provider/<service_provider_id>/resources/requirement/<requirement_id>/<preview_type>')
class ResourcePreviewSmallLarge(OslcResource):

    def get(self, service_provider_id, requirement_id, preview_type):
        endpoint_url = url_for('{}.{}'.format(request.blueprint, self.endpoint),
                               service_provider_id=service_provider_id, requirement_id=requirement_id,
                               preview_type=preview_type)
        base_url = '{}{}'.format(request.url_root.rstrip('/'), endpoint_url)

        requirement = get_requirement(base_url, requirement_id)

        template = "dialogs/"
        if preview_type == 'smallPreview':
            template += "smallpreview.html"

        if preview_type == 'largePreview':
            template += "/largepreview.html"

        response = make_response(render_template(template, title='small', requirement=requirement))

        response.headers['Content-Type'] = 'text/html;charset=UTF-8'
        response.headers['OSLC-Core-Version'] = "2.0"

        return response


@adapter_ns.route('/resourceShapes/<shape_name>')
@api.representation('application/rdf+xml')
@api.representation('application/json-ld')
@api.representation('text/turtle')
class ResourceShapeEndpoint(OslcResource):

    def get(self, shape_name):
        super().get()
        endpoint_url = url_for(
            '{}.{}'.format(request.blueprint, self.endpoint),
            shape_name=shape_name,
        )
        base_url = '{}{}'.format(request.url_root.rstrip('/'), endpoint_url)

        if shape_name == 'requirement':
            shape = build_requirement_shape(base_url)
        elif shape_name == 'sysmlElement':
            shape = build_sysml_element_shape(base_url)
        elif shape_name == 'sysmlRelationship':
            shape = build_sysml_relationship_shape(base_url)
        elif shape_name == 'sysmlNamespace':
            shape = build_sysml_namespace_shape(base_url)
        elif shape_name == 'sysmlType':
            shape = build_sysml_type_shape(base_url)
        elif shape_name == 'sysmlPackage':
            shape = build_sysml_package_shape(base_url)
        elif shape_name == 'sysmlDefinition':
            shape = build_sysml_definition_shape(base_url)
        elif shape_name == 'sysmlUsage':
            shape = build_sysml_usage_shape(base_url)
        elif shape_name == 'sysmlItemDefinition':
            shape = build_sysml_item_definition_shape(base_url)
        elif shape_name == 'sysmlItemUsage':
            shape = build_sysml_item_usage_shape(base_url)
        elif shape_name == 'sysmlPartDefinition':
            shape = build_sysml_part_definition_shape(base_url)
        elif shape_name == 'sysmlPartUsage':
            shape = build_sysml_part_usage_shape(base_url)
        elif shape_name == 'sysmlPortDefinition':
            shape = build_sysml_port_definition_shape(base_url)
        elif shape_name == 'sysmlPortUsage':
            shape = build_sysml_port_usage_shape(base_url)
        elif shape_name == 'sysmlRequirementDefinition':
            shape = build_sysml_requirement_definition_shape(base_url)
        elif shape_name == 'sysmlRequirementUsage':
            shape = build_sysml_requirement_usage_shape(base_url)
        elif shape_name == 'sysmlConcernDefinition':
            shape = build_sysml_concern_definition_shape(base_url)
        elif shape_name == 'sysmlConcernUsage':
            shape = build_sysml_concern_usage_shape(base_url)
        elif shape_name == 'sysmlActionDefinition':
            shape = build_sysml_action_definition_shape(base_url)
        elif shape_name == 'sysmlActionUsage':
            shape = build_sysml_action_usage_shape(base_url)
        elif shape_name == 'sysmlStateDefinition':
            shape = build_sysml_state_definition_shape(base_url)
        elif shape_name == 'sysmlStateUsage':
            shape = build_sysml_state_usage_shape(base_url)
        elif shape_name == 'sysmlConstraintDefinition':
            shape = build_sysml_constraint_definition_shape(base_url)
        elif shape_name == 'sysmlConstraintUsage':
            shape = build_sysml_constraint_usage_shape(base_url)
        elif shape_name == 'sysmlViewDefinition':
            shape = build_sysml_view_definition_shape(base_url)
        elif shape_name == 'sysmlViewUsage':
            shape = build_sysml_view_usage_shape(base_url)
        elif shape_name == 'sysmlViewpointDefinition':
            shape = build_sysml_viewpoint_definition_shape(base_url)
        elif shape_name == 'sysmlViewpointUsage':
            shape = build_sysml_viewpoint_usage_shape(base_url)
        elif shape_name == 'sysmlFeature':
            shape = build_sysml_feature_shape(base_url)
        elif shape_name == 'sysmlClassifier':
            shape = build_sysml_classifier_shape(base_url)
        elif shape_name == 'sysmlOccurrenceDefinition':
            shape = build_sysml_occurrence_definition_shape(base_url)
        elif shape_name == 'sysmlOccurrenceUsage':
            shape = build_sysml_occurrence_usage_shape(base_url)
        elif shape_name == 'sysmlClass':
            shape = build_sysml_class_shape(base_url)
        elif shape_name == 'sysmlStructure':
            shape = build_sysml_structure_shape(base_url)
        elif shape_name == 'sysmlDataType':
            shape = build_sysml_data_type_shape(base_url)
        elif shape_name == 'sysmlBehavior':
            shape = build_sysml_behavior_shape(base_url)
        elif shape_name == 'sysmlFunction':
            shape = build_sysml_function_shape(base_url)
        elif shape_name == 'sysmlPredicate':
            shape = build_sysml_predicate_shape(base_url)
        elif shape_name == 'sysmlLibraryPackage':
            shape = build_sysml_library_package_shape(base_url)
        elif shape_name == 'sysmlAttributeDefinition':
            shape = build_sysml_attribute_definition_shape(base_url)
        elif shape_name == 'sysmlAttributeUsage':
            shape = build_sysml_attribute_usage_shape(base_url)
        elif shape_name == 'sysmlEnumerationDefinition':
            shape = build_sysml_enumeration_definition_shape(base_url)
        elif shape_name == 'sysmlEnumerationUsage':
            shape = build_sysml_enumeration_usage_shape(base_url)
        elif shape_name == 'sysmlCalculationDefinition':
            shape = build_sysml_calculation_definition_shape(base_url)
        elif shape_name == 'sysmlCalculationUsage':
            shape = build_sysml_calculation_usage_shape(base_url)
        elif shape_name == 'sysmlCaseDefinition':
            shape = build_sysml_case_definition_shape(base_url)
        elif shape_name == 'sysmlCaseUsage':
            shape = build_sysml_case_usage_shape(base_url)
        elif shape_name == 'sysmlUseCaseDefinition':
            shape = build_sysml_use_case_definition_shape(base_url)
        elif shape_name == 'sysmlUseCaseUsage':
            shape = build_sysml_use_case_usage_shape(base_url)
        elif shape_name == 'sysmlAnalysisCaseDefinition':
            shape = build_sysml_analysis_case_definition_shape(base_url)
        elif shape_name == 'sysmlAnalysisCaseUsage':
            shape = build_sysml_analysis_case_usage_shape(base_url)
        elif shape_name == 'sysmlVerificationCaseDefinition':
            shape = build_sysml_verification_case_definition_shape(base_url)
        elif shape_name == 'sysmlVerificationCaseUsage':
            shape = build_sysml_verification_case_usage_shape(base_url)
        elif shape_name == 'sysmlConnectionDefinition':
            shape = build_sysml_connection_definition_shape(base_url)
        elif shape_name == 'sysmlConnectionUsage':
            shape = build_sysml_connection_usage_shape(base_url)
        elif shape_name == 'sysmlFlowDefinition':
            shape = build_sysml_flow_definition_shape(base_url)
        elif shape_name == 'sysmlFlowUsage':
            shape = build_sysml_flow_usage_shape(base_url)
        elif shape_name == 'sysmlInterfaceDefinition':
            shape = build_sysml_interface_definition_shape(base_url)
        elif shape_name == 'sysmlInterfaceUsage':
            shape = build_sysml_interface_usage_shape(base_url)
        elif shape_name == 'sysmlAllocationDefinition':
            shape = build_sysml_allocation_definition_shape(base_url)
        elif shape_name == 'sysmlAllocationUsage':
            shape = build_sysml_allocation_usage_shape(base_url)
        elif shape_name == 'sysmlRenderingDefinition':
            shape = build_sysml_rendering_definition_shape(base_url)
        elif shape_name == 'sysmlRenderingUsage':
            shape = build_sysml_rendering_usage_shape(base_url)
        elif shape_name == 'sysmlReferenceUsage':
            shape = build_sysml_reference_usage_shape(base_url)
        elif shape_name == 'sysmlConjugatedPortDefinition':
            shape = build_sysml_conjugated_port_definition_shape(base_url)
        elif shape_name == 'sysmlConnectorAsUsage':
            shape = build_sysml_connector_as_usage_shape(base_url)
        elif shape_name == 'sysmlSuccessionAsUsage':
            shape = build_sysml_succession_as_usage_shape(base_url)
        elif shape_name == 'sysmlBindingConnectorAsUsage':
            shape = build_sysml_binding_connector_as_usage_shape(base_url)
        else:
            raise NotFound()

        shape.to_rdf(self.graph)

        validate_url = request.args.get('validate')
        if validate_url:
            self._run_validation(validate_url)

        return self.create_response(graph=self.graph)

    def _run_validation(self, validate_url):
        import urllib.request

        try:
            req = urllib.request.Request(
                validate_url,
                headers={'Accept': 'text/turtle, application/rdf+xml;q=0.9, application/ld+json;q=0.8'}
            )
            with urllib.request.urlopen(req, timeout=30) as resp:
                resource_data = resp.read()

            content_type = resp.headers.get('Content-Type', '')
            fmt = 'turtle'
            if 'application/rdf+xml' in content_type:
                fmt = 'xml'
            elif 'application/ld+json' in content_type:
                fmt = 'json-ld'

            resource_graph = Graph()
            resource_graph.parse(data=resource_data, format=fmt)

            shacl_graph = oslc_shape_to_shacl(self.graph)
            _, results_graph, results_text = validate_resource(resource_graph, shacl_graph)

            self.graph += results_graph
        except Exception as exc:
            err_g = Graph()
            err_g.bind('sh', 'http://www.w3.org/ns/shacl#')
            ns_sh = rdflib.Namespace('http://www.w3.org/ns/shacl#')
            report = ns_sh.ValidationReport
            result = ns_sh.ValidationResult
            result_node = rdflib.BNode()
            err_g.add((result_node, rdflib.RDF.type, report))
            err_g.add((result_node, ns_sh.conforms, rdflib.Literal(False)))
            err_node = rdflib.BNode()
            err_g.add((result_node, ns_sh.result, err_node))
            err_g.add((err_node, rdflib.RDF.type, result))
            err_g.add((err_node, ns_sh.resultMessage, rdflib.Literal(str(exc))))
            self.graph += err_g

    def options(self, shape_name):
        response = make_response('', 204)
        response.headers['Allow'] = 'GET,OPTIONS,HEAD'
        oslc_version = OslcResource.get_requested_version()
        response.headers['OSLC-Core-Version'] = oslc_version
        return response


@adapter_ns.route('/rootservices')
class RootServices(OslcResource):

    def get(self):

        """
        Generate Rootservices response
        :return:
        """
        super().get()

        endpoint_url = url_for('{}.{}'.format(request.blueprint, self.endpoint))
        base_url = '{}{}'.format(request.url_root.rstrip('/'), endpoint_url)

        rootservices_url = urlparse(base_url).geturl()

        root_services = RootServiceSingleton.get_root_service(rootservices_url)
        root_services.about = request.base_url
        publisher_url = rootservices_url.replace('rootservices', 'publisher')
        root_services.publisher = PublisherSingleton.get_publisher(publisher_url)
        root_services.to_rdf(self.graph)

        return self.create_response(graph=self.graph, rdf_format='rootservices-xml')

    def options(self):
        response = make_response('', 204)
        response.headers['Allow'] = 'GET,OPTIONS,HEAD'
        oslc_version = OslcResource.get_requested_version()
        response.headers['OSLC-Core-Version'] = oslc_version
        return response


@adapter_ns.route('/config')
class ConfigurationCatalog(OslcResource):

    def get(self):
        endpoint_url = url_for('{}.{}'.format(request.blueprint, self.endpoint))
        base_url = '{}{}'.format(request.url_root.rstrip('/'), endpoint_url)

        catalog_url = urlparse(base_url).geturl()

        response = make_response(render_template('pyoslc_oauth/configuration.html',
                                                 about=catalog_url,
                                                 components=catalog_url + '/components'))

        response.headers['max-age'] = '0'
        response.headers['pragma'] = 'no-cache'
        response.headers['Cache-Control'] = 'no-cache'
        response.headers['Content-Length'] = len(response.data)
        response.headers['Content-Type'] = 'application/rdf+xml;charset=UTF-8'
        response.headers['OSLC-Core-Version'] = "2.0"

        return response


@adapter_ns.route('/config/components')
class ConfigurationComponent(OslcResource):

    def get(self):
        super().get()
        endpoint_url = url_for('{}.{}'.format(request.blueprint, self.endpoint))
        base_url = '{}{}'.format(request.url_root.rstrip('/'), endpoint_url)

        components_url = urlparse(base_url).geturl()

        response = make_response(render_template('pyoslc_oauth/components.html',
                                                 about=components_url,
                                                 dialog=components_url.replace('components', 'selection')))

        response.headers['max-age'] = '0'
        response.headers['pragma'] = 'no-cache'
        response.headers['Cache-Control'] = 'no-cache'
        response.headers['Content-Length'] = len(response.data)
        response.headers['Content-Type'] = 'application/rdf+xml;charset=UTF-8'
        response.headers['OSLC-Core-Version'] = "2.0"

        return response


@adapter_ns.route('/config/publisher')
class ConfigurationPublisher(OslcResource):

    def get(self):
        super().get()
        endpoint_url = url_for('{}.{}'.format(request.blueprint, self.endpoint))
        base_url = '{}{}'.format(request.url_root.rstrip('/'), endpoint_url)

        components_url = urlparse(base_url).geturl()

        response = make_response(render_template('pyoslc_oauth/publisher.html', about=components_url))

        response.headers['max-age'] = '0'
        response.headers['pragma'] = 'no-cache'
        response.headers['Cache-Control'] = 'no-cache'
        response.headers['Content-Length'] = len(response.data)
        response.headers['Content-Type'] = 'application/rdf+xml;charset=UTF-8'
        response.headers['OSLC-Core-Version'] = "2.0"

        return response


@adapter_ns.route('/config/selection')
class ConfigurationSelection(OslcResource):

    def get(self):
        endpoint_url = url_for('{}.{}'.format(request.blueprint, self.endpoint))
        base_url = '{}{}'.format(request.url_root.rstrip('/'), endpoint_url)

        components_url = urlparse(base_url).geturl()

        stream = request.args.get('stream')
        if stream:

            result = [
                {
                    'oslc:label': 'PyOSLC Stream 1',
                    'rdf:resource': url_for('oslc.adapter_configuration_stream', stream_id=1, _external=True),
                    'rdf:type': 'http://open-services.net/ns/config#Stream'

                },
                {
                    'oslc:label': 'PyOSLC Stream 2',
                    'rdf:resource': url_for('oslc.adapter_configuration_stream', stream_id=2, _external=True),
                    'rdf:type': 'http://open-services.net/ns/config#Stream'
                }
            ]

            return {"oslc:results": result}, 200

        response = make_response(render_template('pyoslc_oauth/selection.xhtml',
                                                 selection_uri=components_url.replace('components', 'selection')))

        response.headers['max-age'] = '0'
        response.headers['pragma'] = 'no-cache'
        response.headers['Cache-Control'] = 'no-cache'
        response.headers['Content-Length'] = len(response.data)
        response.headers['Content-Type'] = 'application/rdf+xml;charset=UTF-8'
        response.headers['OSLC-Core-Version'] = "2.0"

        return response


@adapter_ns.route('/config/stream/<int:stream_id>')
class ConfigurationStream(OslcResource):

    def get(self, stream_id):
        endpoint_url = url_for('{}.{}'.format(request.blueprint, self.endpoint), stream_id=stream_id)
        base_url = '{}{}'.format(request.url_root.rstrip('/'), endpoint_url)

        stream_url = urlparse(base_url).geturl()

        catalog_url = url_for('oslc.adapter_service_provider_catalog', _external=True)
        service_provider_url = url_for('oslc.adapter_service_provider', service_provider_id='Project-1', _external=True)

        response = make_response(render_template('pyoslc_oauth/stream.html',
                                                 stream_url=stream_url,
                                                 selection_url=url_for('oslc.adapter_configuration_selection',
                                                                       _external=True),
                                                 stream_id=stream_id,
                                                 project_area=catalog_url,
                                                 service_provider_url=service_provider_url,
                                                 selection_uri=stream_url.replace('components', 'selection')))

        response.headers['max-age'] = '0'
        response.headers['pragma'] = 'no-cache'
        response.headers['Cache-Control'] = 'no-cache'
        response.headers['Content-Length'] = len(response.data)
        response.headers['Content-Type'] = 'application/rdf+xml;charset=UTF-8'
        response.headers['OSLC-Core-Version'] = "2.0"

        return response


@adapter_ns.route('/scr')
class Source(OslcResource):

    def get(self):
        response = make_response(render_template('pyoslc_oauth/scr.html'))
        return response
