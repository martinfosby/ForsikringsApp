from cgitb import text
import select
from flask import render_template, request, redirect, session,flash,url_for
from flask_login import login_required, login_user, logout_user, current_user
from app.blueprints.main import bp
from app.extensions import login_manager, db
from app.blueprints.auth.login_manager import load_user


@bp.route('/')
@bp.route('/index')
@bp.route('/home', endpoint='home')
@login_required
def index():
    return render_template('main/index.html')

