from flask_app.app.extensions import db
from flask_app.app.utils import test_db_connection
from flask_login import UserMixin

# sqlalchemy init

class User(db.Model, UserMixin):
    __table__ = db.metadata.tables["user"]
   

class InsuranceCompany(db.Model):
    __table__ = db.metadata.tables["insurance_company"]


class Contact(db.Model):
    __table__ = db.metadata.tables["contact"]


class UnitType(db.Model):
    __table__ = db.metadata.tables["unit_type"]


class Insurance(db.Model):
    __table__ = db.metadata.tables["insurance"]


class Offer(db.Model):
    __table__ = db.metadata.tables["offer"]


class Settlement(db.Model):
    __table__ = db.metadata.tables["settlement"]