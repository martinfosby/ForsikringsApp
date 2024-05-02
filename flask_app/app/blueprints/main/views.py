from flask import g, render_template, request, redirect, session
from flask_login import login_required, current_user
from app.blueprints.main import bp
from app.utils import url_has_allowed_host_and_scheme

@bp.route('/')
@bp.route('/index')
@bp.route('/home', endpoint='home')
@login_required
def index():
    return render_template('main/index.html')

