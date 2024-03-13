from flask import Blueprint

bp = Blueprint("auth", __name__, static_folder="static", template_folder="templates", url_prefix="/auth")

from flask_app.app.blueprints.auth import views