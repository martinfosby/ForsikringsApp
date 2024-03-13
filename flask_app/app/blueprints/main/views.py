from flask import render_template, request, redirect, session,flash,url_for
from flask_login import login_required, login_user, logout_user, current_user, LoginManager
from flask_app.app.utils import set_password, check_password_hash
from flask_app.app.blueprints.main import bp


@bp.route('/')
def index():
    return render_template('base.html', title='test')


@bp.route('/works')
def works():
    return render_template('base.html', title='its working')