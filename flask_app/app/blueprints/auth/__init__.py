from flask import Blueprint

bp = Blueprint("auth", __name__, static_folder="static")

from . import views