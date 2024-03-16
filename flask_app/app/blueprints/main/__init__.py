from flask import Blueprint


bp = Blueprint("main", __name__, static_folder="static")

from . import views