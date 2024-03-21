from flask import Blueprint


bp = Blueprint('testing', __name__)

from . import views