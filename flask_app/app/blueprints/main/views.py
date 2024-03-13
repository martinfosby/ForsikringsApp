from flask import render_template, request, redirect, session,flash,url_for
from flask_login import login_required, login_user, logout_user, current_user
from flask_app.app.utils import set_password, check_password
from flask_app.app.blueprints.main import bp


@bp.route('/')
def index():
    if current_user.is_authenticated:
        return render_template('base.html', title=f'Logged in as {current_user.username}')
    else:
        return redirect(url_for('auth.login'))
