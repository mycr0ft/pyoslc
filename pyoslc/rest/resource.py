import logging

from flask import request, make_response
from flask_restx import Resource
from rdflib import Graph, RDF, RDFS, DCTERMS
from rdflib.plugin import PluginException
from werkzeug.exceptions import UnsupportedMediaType

from pyoslc.vocabularies.core import OSLC
from pyoslc.vocabularies.jazz import JAZZ_PROCESS

logger = logging.getLogger(__name__)


class OslcResource(Resource):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.graph = kwargs.get('graph', Graph())
        self.graph.bind('oslc', OSLC)
        self.graph.bind('rdf', RDF)
        self.graph.bind('rdfs', RDFS)
        self.graph.bind('dcterms', DCTERMS)
        self.graph.bind('j.0', JAZZ_PROCESS)

    def get(self, *args, **kwargs):
        accept = request.headers.get('accept')
        logger.debug("accept: {}".format(accept))
        if not (accept in ('application/rdf+xml', 'application/json',
                           'application/ld+json', 'application/json-ld',
                           'application/xml', 'application/atom+xml',
                           'text/turtle',
                           'application/xml, application/x-oslc-cm-service-description+xml',
                           'application/x-oslc-compact+xml, application/x-jazz-compact-rendering; q=0.5',
                           'application/rdf+xml,application/x-turtle,application/ntriples,application/json')):
            raise UnsupportedMediaType

    @staticmethod
    def get_requested_version():
        version = request.headers.get('OSLC-Core-Version', '2.0')
        if version in ('2.0', '3.0'):
            return version
        return '2.0'

    @staticmethod
    def create_response(graph, accept=None, content=None, rdf_format=None, etag=False):

        accept = accept if accept is not None else request.headers.get('accept', 'application/rdf+xml')
        content = content if content is not None else request.headers.get('content-type', accept)
        if content.__contains__('x-www-form-urlencoded') or content.__contains__('text/plain'):
            content = accept

        rdf_format = accept if rdf_format is None else rdf_format

        if accept in ('application/json-ld', 'application/ld+json', 'application/json', '*/*'):
            rdf_format = 'json-ld'

        if rdf_format in ('application/xml', 'application/rdf+xml'):
            rdf_format = 'pretty-xml'

        if rdf_format == 'text/turtle':
            rdf_format = 'turtle'

        if rdf_format.__contains__('rootservices-xml') and (not accept.__contains__('xml')):
            rdf_format = accept

        if rdf_format == 'application/atom+xml':
            rdf_format = 'pretty-xml'

        if rdf_format in ('application/xml, application/x-oslc-cm-service-description+xml'):
            rdf_format = 'pretty-xml'
            content = 'application/rdf+xml'

        try:
            logger.debug('Parsing the Graph into {}'.format(rdf_format))
            data = graph.serialize(format=rdf_format)
        except PluginException as pe:
            response_object = {
                'status': 'fail',
                'message': 'Content-Type Incompatible: {}'.format(pe)
            }
            return response_object, 400

        oslc_version = OslcResource.get_requested_version()

        response = make_response(data.decode('utf-8') if not isinstance(data, str) else data, 200)
        response.headers['Accept'] = accept
        response.headers['Content-Type'] = content
        response.headers['OSLC-Core-Version'] = oslc_version

        if etag:
            response.add_etag()

        return response
