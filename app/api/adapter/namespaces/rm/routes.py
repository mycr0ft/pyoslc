import logging
import os

from flask import request, render_template, make_response, current_app
from flask_restx import Resource
from rdflib import Graph, RDF, DCTERMS
from rdflib.plugin import PluginException

from app.api.adapter import api
from app.api.adapter.exceptions import NotModified
from app.api.adapter.mappings.specification import specification_map
from app.api.adapter.namespaces.business import (
    create_requirement,
    delete_requirement,
    get_requirement,
    get_requirement_list,
    update_requirement,
)
from app.api.adapter.namespaces.rm.models import specification
from app.api.adapter.namespaces.rm.parsers import (
    specification_parser,
    csv_file_upload,
)
from pyoslc.vocabularies.core import OSLC
from pyoslc.vocabularies.rm import OSLC_RM

logger = logging.getLogger(__name__)

attributes = specification_map


class RequirementList(Resource):

    @api.response(200, 'The RDF formatted response of the requirements, taken from the specification')
    def get(self):
        try:
            content_type = request.headers['accept']
            if content_type in ('application/json-ld', 'application/json'):
                content_type = 'json-ld'

            requirements = get_requirement_list(request.base_url, '', '')

            graph = Graph()
            graph.bind('oslc', OSLC, override=False)
            graph.bind('dcterms', DCTERMS, override=False)
            graph.bind('oslc_rm', OSLC_RM, override=False)

            for requirement in requirements:
                graph += requirement.to_rdf(graph, request.base_url, attributes)

            if 'text/html' in content_type:
                requirements = list()
                for r in graph.subjects(RDF.type, OSLC_RM.Requirement):
                    requirements.append(r)

                response = make_response(render_template('web/requirement_list.html',
                                                         requirements=requirements), 200)
            else:
                data = graph.serialize(format=content_type)

                response = make_response(data.decode('utf-8') if not isinstance(data, str) else data, 200)
                response.headers['Content-Type'] = content_type
                response.headers['Oslc-Core-Version'] = "2.0"

            return response

        except PluginException as pe:
            response_object = {
                'status': 'fail',
                'message': 'Content-Type Incompatible: {}'.format(pe)
            }
            return response_object, 400

        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': 'An exception has occurred: {}'.format(e)
            }
            return response_object, 500

    @api.expect(specification)
    @api.response(201, 'Specification successfully created.')
    def post(self):
        content_type = request.headers['content-type']
        logger.debug('content-type: {}'.format(content_type))
        if content_type != 'application/rdf+xml':
            data = specification_parser.parse_args()
        else:
            print('TODO - transform from rdf')
            data = None

        result = create_requirement(data)

        if isinstance(result, NotModified):
            response_object = {
                'status': 'fail',
                'message': 'Not Modified'
            }
            return response_object, 304

        if result is None:
            response_object = {
                'status': 'fail',
                'message': 'Not Found'
            }
            return response_object, 400

        response = make_response('', 201)
        response.headers['Location'] = result.about

        logger.debug('Adding the resource from the RM endpoint')

        return response


class RequirementItem(Resource):

    def get(self, id):
        try:
            content_type = request.headers['accept']
            if content_type in ('application/json-ld', 'application/json'):
                content_type = 'json-ld'

            graph = Graph()

            r = get_requirement(request.base_url, id)
            graph = r.to_rdf(graph, request.base_url, attributes)

            if 'text/html' in content_type:
                response = make_response(render_template('web/requirement.html', id=id, statements=graph), 200)
            else:
                data = graph.serialize(format=content_type)

                response = make_response(data.decode('utf-8') if not isinstance(data, str) else data, 200)
                response.headers['Content-Type'] = content_type
                response.headers['Oslc-Core-Version'] = "2.0"

            return response

        except PluginException as pe:
            response_object = {
                'status': 'fail',
                'message': 'Content-Type Incompatible: {}'.format(pe)
            }
            return response_object, 400

        except Exception as e:
            response_object = {
                'status': 'fail',
                'message': 'An exception has ocurred: {}'.format(e)
            }
            return response_object, 500

    @api.expect(specification)
    def put(self, id):
        data = specification_parser.parse_args()

        if data:
            result = update_requirement(id, data)

            if isinstance(result, NotModified):
                return make_response('{Not Modified}', 304)

        return make_response('{}', 200)

    def delete(self, id):
        result = delete_requirement(id)

        if isinstance(result, NotModified):
            return make_response('{Not Modified}', 304)

        return make_response('{}', 200)


class UploadCollection(Resource):

    @api.expect(csv_file_upload)
    def post(self):
        args = csv_file_upload.parse_args()
        if args['csv_file'].mimetype in ('application/xls', 'text/csv'):
            destination = os.path.join(current_app.instance_path, 'medias/')
            if not os.path.exists(destination):
                os.makedirs(destination)
            csv_file = f'{destination}custom_file_name.csv'
            args['csv_file'].save(csv_file)

        else:
            return make_response('{Bad request}', 404)

        return make_response('{\'status\': \'Done\'}', 200)
