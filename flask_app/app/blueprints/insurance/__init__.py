from flask import Blueprint

bp = Blueprint("insurance", __name__, static_folder="static", template_folder="templates")


from flask_app.app.blueprints.insurance import views
