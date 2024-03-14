from flask import render_template, request, redirect, session,flash,url_for
from flask_login import login_required, login_user, logout_user, current_user
from flask_app.app.utils import set_password, check_password
from flask_app.app.blueprints.main import bp
from flask_app.app.extensions import login_manager, db
from flask_app.app.blueprints.auth.login_manager import load_user

from flask_app.app.models.meta import UserMeta



@bp.route('/')
@login_required
def index():
    return render_template('base.html', title=f'Logged in as {current_user.username}')



@bp.route('/meta/add')
def metaDbTest():
    user = UserMeta(username='testuser', password_hash='foekfeok')
    login_user(user)
    return render_template('base.html', title=f'Logged in as {current_user.username}')
