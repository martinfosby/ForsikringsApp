from flask import abort, render_template, request, redirect, session,flash,url_for
from flask_login import login_required, login_user, logout_user, current_user
from app.extensions import db, login_manager
from app.models import Customer
from app.blueprints.auth import bp
from res import string_resource

login_manager.login_view = f"{bp.name}.login"
login_manager.refresh_view = f"{bp.name}.login"
login_manager.login_message_category = "info"
login_manager.session_protection = "basic" # set to either None "basic" or "Strong", by default is basic
login_manager.login_message = string_resource("login_required")
login_manager.needs_refresh_message = string_resource("login_fresh")



@login_manager.user_loader
def load_user(user_id):
    return db.session.query(Customer).get(user_id)

