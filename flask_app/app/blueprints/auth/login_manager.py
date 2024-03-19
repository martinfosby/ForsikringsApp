from flask import abort, render_template, request, redirect, session,flash,url_for
from flask_login import login_required, login_user, logout_user, current_user
from flask_app.app.extensions import db, login_manager
from flask_app.app.models import Customer
from flask_app.app.blueprints.auth import bp

login_manager.login_view = f"{bp.name}.login"
login_manager.refresh_view = f"{bp.name}.login"
login_manager.login_message = "You must be logged in to access this page."
login_manager.login_message_category = "info"
login_manager.needs_refresh_message = "You need to log in again!"
login_manager.session_protection = "basic" # set to either None "basic" or "Strong", by default is basic



@login_manager.user_loader
def load_user(user_id):
    return db.session.query(Customer).get(user_id)

# @login_manager.unauthorized_handler
# def unauthorized_callback():
#     return redirect(url_for("auth.login"))
