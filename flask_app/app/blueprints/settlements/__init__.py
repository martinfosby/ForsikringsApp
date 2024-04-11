from flask import Blueprint

bp = Blueprint("settlements", __name__, static_folder="static")

from . import views