from flask import Blueprint

bp = Blueprint("local", __name__, static_folder="static")

from . import views