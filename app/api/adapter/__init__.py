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
