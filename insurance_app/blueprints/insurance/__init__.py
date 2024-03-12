from flask import Blueprint

insurance_bp = Blueprint("insurance", __name__, static_folder="static", template_folder="templates")


