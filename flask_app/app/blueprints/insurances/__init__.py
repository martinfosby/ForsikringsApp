from flask import Blueprint

bp = Blueprint("insurances", __name__, static_folder="static")

from . import views


