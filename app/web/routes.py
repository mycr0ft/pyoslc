from flask import Blueprint, render_template, redirect, url_for

bp = Blueprint('web', __name__, template_folder='templates')


@bp.route('/')
def index():
    return render_template("web/index.html")


@bp.route('/.well-known/oslc/sp-catalog')
def oslc_sp_catalog():
    return redirect(url_for('oslc.adapter_service_provider_catalog'))
