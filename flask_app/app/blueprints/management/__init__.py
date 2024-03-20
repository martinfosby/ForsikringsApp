from flask_app.app.extensions import admin, db
from flask_admin.contrib.sqla import ModelView
from flask_app.app.models import *
from flask.blueprints import Blueprint


bp = Blueprint("management", __name__, static_folder="static")

admin.add_view(ModelView(Customer, db.session))
admin.add_view(ModelView(Insurance, db.session))
admin.add_view(ModelView(Company, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(Settlement, db.session))
admin.add_view(ModelView(Offer, db.session))
admin.add_view(ModelView(Contact, db.session))