import logging

from flask import Blueprint, request
from flask_restx import Api
from werkzeug.exceptions import HTTPException

from pyoslc.rest.resource import OslcResource

bp = Blueprint('oslc', __name__, url_prefix='/services', static_folder='static')

api = Api(
    app=bp,
    version='1.0.0',
    title='Python OSLC API',
    description='Implementation for the OSLC specification for python application',
    contact='Contact Software & Koneksys',
    contact_url='https://www.contact-software.com/en/',
    contact_email="mario.carrasco@koneksys.com",
    validate=True
)


@bp.app_errorhandler(500)
def internal_error(error):
    logger = logging.getLogger('flask.app')
    logger.debug('Requesting INTERNAL_ERROR from: {}'.format(request.base_url))
    return OslcResource.build_error_response(500, 'Internal Server Error')


@bp.app_errorhandler(404)
def not_found_error(error):
    logger = logging.getLogger('flask.app')
    logger.debug('Requesting 404 from: {}'.format(request.base_url))
    msg = str(error) if isinstance(error, HTTPException) else 'Not Found'
    return OslcResource.build_error_response(404, msg)


@bp.app_errorhandler(400)
def bad_request_error(error):
    logger = logging.getLogger('flask.app')
    logger.debug('Requesting 400 from: {}'.format(request.base_url))
    msg = str(error) if isinstance(error, HTTPException) else 'Bad Request'
    return OslcResource.build_error_response(400, msg)


@bp.app_errorhandler(415)
def unsupported_media_type_error(error):
    logger = logging.getLogger('flask.app')
    logger.debug('Requesting 415 from: {}'.format(request.base_url))
    return OslcResource.build_error_response(415, 'Unsupported Media Type')


@bp.app_errorhandler(406)
def not_acceptable_error(error):
    logger = logging.getLogger('flask.app')
    logger.debug('Requesting 406 from: {}'.format(request.base_url))
    return OslcResource.build_error_response(406, 'Not Acceptable')


@bp.before_request
def before_request_func():
    logger = logging.getLogger('flask.app')
    logger.debug('Requesting BEFORE_REQUEST from: {} {} to {}'.format(request.access_route,
                                                                      request.user_agent,
                                                                      request.base_url))
    logger.debug('Request Referrer {}'.format(request.referrer))


@api.errorhandler
def default_error_handler(e):
    if isinstance(e, HTTPException):
        return OslcResource.build_error_response(e.code, str(e))
    return OslcResource.build_error_response(500, str(e))


def register_representations(api) -> None:
    """Called from oslc.init_app AFTER all namespaces import — re-registers
    the real serializers, undoing the class-as-representation bug from
    core.py's @api.representation-decorated resource classes."""
    api.representation("application/rdf+xml")(represent_rdf_xml)
    api.representation("application/json-ld")(represent_jsonld)
    api.representation("text/turtle")(represent_turtle)
    api.representation("application/json")(represent_json)


# ---------------------------------------------------------------------------
# representation (serializer) functions — ROOT-CAUSE FIX for the
# 'ResourceShapeEndpoint' object has no attribute 'headers' crash on any
# flask-restx error path.
#
# flask-restx's @api.representation decorator registers a function that
# turns a marshalled payload into a Response.  core.py decorated
# Resource CLASSES with it, so flask_restx stored the class as the
# serializer; when a Resource returns (dict, status) — every error
# path in every namespace — make_response calls
# representations[mediatype](data, code, headers) which resolves to the
# class constructor and then crashes on .headers.  Any error response
# (404/400/500 from a flask-restx resource) reproduced it; the reason
# it lurked so long is that the happy paths all return real Response
# objects via OslcResource.create_response, bypassing the serializer.
#
# Fix: register real serializer functions.  build_error_response already
# renders a proper OSLC Error document; these serializers pass
# marshalled payloads (dicts/Response) through with the right
# Content-Type.
# ---------------------------------------------------------------------------

def _serialize_payload(data, code, headers, content_type):
    from flask import make_response as _make_response
    import json as _json

    if isinstance(data, tuple) and len(data) == 2 and \
            isinstance(data[1], int) and not hasattr(data, 'headers'):
        # (payload, status) tuple from a Resource
        payload, status = data
        response = _make_response(payload, status)
    elif isinstance(data, dict):
        response = _make_response(_json.dumps(data), code or 200)
    elif hasattr(data, 'headers'):     # already a Response
        response = data
        if code is not None and response.status_code != code:
            response.status_code = code
    else:
        response = _make_response(data, code or 200)
    if response.headers.get('Content-Type') in (None, '') or \
            not hasattr(data, 'headers') and response.mimetype == 'text/html':
        response.headers['Content-Type'] = content_type
    for k, v in (headers or {}).items():
        response.headers[k] = v
    return response


def represent_rdf_xml(data, code=200, headers=None):
    return _serialize_payload(data, code, headers,
                              'application/rdf+xml; charset=UTF-8')


def represent_jsonld(data, code=200, headers=None):
    return _serialize_payload(data, code, headers, 'application/json-ld')


def represent_turtle(data, code=200, headers=None):
    return _serialize_payload(data, code, headers, 'text/turtle')


def represent_json(data, code=200, headers=None):
    return _serialize_payload(data, code, headers, 'application/json')
