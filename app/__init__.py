import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask, request


def create_app(app_config=None):
    app = Flask(__name__, instance_relative_config=False)

    if app_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_object(app_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    if not app.debug and not app.testing:
        if app.config['MAIL_SERVER']:
            """
            Implementation for Mail notifications
            """
            pass

    if app.debug and app.config['LOG_TO_STDOUT']:
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(logging.INFO)
        app.logger.addHandler(stream_handler)
    else:
        if not os.path.exists('logs'):
            os.mkdir('logs')

        file_handler = RotatingFileHandler('logs/pysolc.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter('%(asctime)s '
                                                    '%(levelname)s: %(message)s '
                                                    '[in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('---------- Initializing PyOSL WS-API ----------')

    from .web.routes import bp as website
    app.register_blueprint(website)

    from app.api.adapter import oslc
    oslc.init_app(app)

    from app.api.oauth import oslc_oauth
    oslc_oauth.init_app(app)

    if app.config.get('SYSML_MODEL_PATH'):
        from app.api.adapter.namespaces.sysml.seeder import seed_saturn_v
        seed_saturn_v(app.config['SYSML_MODEL_PATH'])

    # STEP side of the Vee: seed demo STEP models when configured
    # (STEP_FIXTURES env — os.pathsep-separated .stp paths — or the
    # STEP_FIXTURES config key; matches the sysml seeder convention).
    from app.api.adapter.namespaces.step.seeder import seed_app_models
    seed_app_models(app)

    # --- CORS for browser OSLC consumers (the web viewer MVP) ---------
    # The MVP viewer is a STATIC page (file:// or another origin) that
    # fetches RDF/JSON from this server. Browsers block cross-origin
    # fetches without these headers. Dev-friendly by default; lock
    # down via CORS_ORIGINS config when deployed.
    @app.after_request
    def _cors_headers(response):
        origins = app.config.get('CORS_ORIGINS', '*')
        if origins == '*':
            response.headers['Access-Control-Allow-Origin'] = '*'
        else:
            request_origin = request.headers.get('Origin')
            if request_origin and request_origin in origins:
                response.headers['Access-Control-Allow-Origin'] = request_origin
                response.headers['Vary'] = 'Origin'
        response.headers['Access-Control-Allow-Headers'] = \
            'Content-Type, Authorization, Accept'
        response.headers['Access-Control-Allow-Methods'] = \
            'GET, POST, OPTIONS'
        return response

    @app.route('/oslc/<path:_any>', methods=['OPTIONS'])
    def _oslc_preflight(_any):          # flask-restx OPTIONS is uneven; preflight here
        return '', 204

    return app
