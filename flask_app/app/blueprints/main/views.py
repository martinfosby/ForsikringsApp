from flask import g, render_template, request, redirect, session
from flask_login import login_required, current_user
from app.blueprints.main import bp

@bp.route('/')
@bp.route('/index')
@bp.route('/home', endpoint='home')
def index():
    return render_template('main/index.html')
