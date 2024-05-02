from flask import redirect, url_for
from app.extensions import admin, db
from flask_admin.contrib.sqla import ModelView 
from app.models import *
from flask.blueprints import Blueprint
from flask_admin import BaseView, expose



bp = Blueprint("administrator", __name__, static_folder="static")

class HomeView(BaseView):
    @expose('/')
    def index(self):
        return redirect(url_for('main.index'))


admin.add_view(ModelView(Customer, db.session))
admin.add_view(ModelView(Insurance, db.session))
admin.add_view(ModelView(Company, db.session))
admin.add_view(ModelView(UnitType, db.session))
admin.add_view(ModelView(Settlement, db.session))
admin.add_view(ModelView(Offer, db.session))
admin.add_view(ModelView(Contact, db.session))
admin.add_view(HomeView(name='Home', endpoint='home'))