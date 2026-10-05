from app.api.adapter import bp, api
from app.api.adapter.dialogs.routes import dialog_bp
from app.api.adapter.namespaces.config.routes import config_ns
from app.api.adapter.namespaces.core import adapter_ns
from app.api.adapter.namespaces.rm import rm_ns
from app.api.adapter.namespaces.step import step_ns
from app.api.adapter.namespaces.sysml import sysml_ns

from app.api.adapter import register_representations


def init_app(app):
    app.register_blueprint(bp, url_prefix='/oslc')
    api.add_namespace(adapter_ns)
    api.add_namespace(rm_ns)
    api.add_namespace(config_ns)
    api.add_namespace(sysml_ns)
    api.add_namespace(step_ns)
    # Register the real serializers LAST: core.py decorates resource
    # classes with @api.representation (a flask-restx misuse — class
    # objects end up stored as serializers) and would otherwise
    # overwrite the real ones. See __init__.py (root-cause note).
    register_representations(api)
    app.register_blueprint(dialog_bp, url_prefix='/oslc/services')
