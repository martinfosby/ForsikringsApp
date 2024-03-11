from flask import Blueprint
from user_bp.login import login

user_bp = Blueprint('user_bp', __name__, template_folder='templates', static_folder='static')


__all__ = [user_bp, login]
