from flask import Blueprint

bp = Blueprint("contacts", __name__, static_folder="static")

from . import views


