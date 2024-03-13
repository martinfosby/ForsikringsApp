from flask import Blueprint

bp = Blueprint("user", __name__, static_folder="static", template_folder="templates")


from flask_app.app.blueprints.user import views