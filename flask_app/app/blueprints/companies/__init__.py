from flask import Blueprint

bp = Blueprint("companies", __name__, static_folder="static")

from . import views


