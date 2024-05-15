from flask import Blueprint

bp = Blueprint("unit_types", __name__, static_folder="static")

from . import views


