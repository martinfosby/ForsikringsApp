from flask_app.app.extensions import admin, db
from flask_admin.contrib.sqla import ModelView
from flask_app.app.models import *
from flask.blueprints import Blueprint


bp = Blueprint("management", __name__, static_folder="static")

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Insurance, db.session))
admin.add_view(ModelView(InsuranceCompany, db.session))
admin.add_view(ModelView(UnitType, db.session))
admin.add_view(ModelView(Settlement, db.session))
admin.add_view(ModelView(Offer, db.session))
admin.add_view(ModelView(Contact, db.session))