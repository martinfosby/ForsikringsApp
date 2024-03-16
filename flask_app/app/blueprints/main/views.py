from flask import render_template, request, redirect, session,flash,url_for
from flask_login import login_required, login_user, logout_user, current_user
from flask_app.app.blueprints.main import bp
from flask_app.app.extensions import login_manager, db
from flask_app.app.blueprints.auth.login_manager import load_user


@bp.route('/')
@login_required
def index():
    return render_template('main/index.html')

