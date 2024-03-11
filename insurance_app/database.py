from insurance_app import app, db
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import inspect
from flask_login import UserMixin, login_required, login_user, logout_user, current_user, LoginManager

with app.app_context():
    Base = automap_base()
    Base.prepare(db.engine, reflect=True)



# class User(Base.classes.user, UserMixin):
#     pass



User = Base.classes.user
Contact = Base.classes.contact
Insurance = Base.classes.insurance
InsuranceCompany = Base.classes.insurance_company
Offer = Base.classes.offer
Settlement = Base.classes.settlement
UnitType = Base.classes.unit_type


