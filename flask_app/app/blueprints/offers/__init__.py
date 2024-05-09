from flask import Blueprint

bp = Blueprint("offers", __name__, static_folder="static")

from . import views


