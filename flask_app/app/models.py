from flask_app.app.extensions import db
from flask_login import UserMixin

# sqlalchemy init

try:
    # Try connecting to the database
    db.reflect()
    with db.engine.connect() as connection:
        print("Connected successfully!")
except Exception as e:
    # If connection fails, print the error
    print("Connection failed:", e)


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