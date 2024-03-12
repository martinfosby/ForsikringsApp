from flask_app.app.extensions import db
from flask import current_app
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
    # id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(45), unique=True)
    # password_hash = db.Column(db.String(128))
    # is_admin = db.Column(db.Boolean)

class InsuranceCompany(db.Model):
    __table__ = db.metadata.tables["insurance_company"]
    # id = db.Column(db.Integer, primary_key=True)
    # name = db.Column(db.String(90))


class Contact(db.Model):
    __table__ = db.metadata.tables["contact"]
    # id = db.Column(db.Integer, primary_key=True)
    # company_id = db.Column(db.Integer, db.ForeignKey('insurance_company.id'))
    # name = db.Column(db.String(90))
    # phone_number = db.Column(db.String(30))
    # email = db.Column(db.String(90))
    # company = db.relationship('InsuranceCompany', backref='contacts')




class UnitType(db.Model):
    __table__ = db.metadata.tables["unit_type"]
    # id = db.Column(db.Integer, primary_key=True)
    # unit_name = db.Column(db.String(90))


class Insurance(db.Model):
    __table__ = db.metadata.tables["insurance"]
    # id = db.Column(db.Integer, primary_key=True)
    # label = db.Column(db.String(90))
    # unit_id = db.Column(db.Integer, db.ForeignKey('unit_type.id'))
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # value = db.Column(db.Integer)
    # price = db.Column(db.Integer)
    # due_date = db.Column(db.Date)
    # company_id = db.Column(db.Integer, db.ForeignKey('insurance_company.id'))
    # unit_type = db.relationship('UnitType', backref='insurances')
    # user = db.relationship('User', backref='insurances')
    # company = db.relationship('InsuranceCompany', backref='insurances')


class Offer(db.Model):
    __table__ = db.metadata.tables["offer"]
    # id = db.Column(db.Integer, primary_key=True)
    # label = db.Column(db.String(90))
    # unit_id = db.Column(db.Integer, db.ForeignKey('insurance.id'))
    # price = db.Column(db.Integer)
    # insurance = db.relationship('Insurance', backref='offers')


class Settlement(db.Model):
    __table__ = db.metadata.tables["settlement"]
#     id = db.Column(db.Integer, primary_key=True)
#     unit_id = db.Column(db.Integer, db.ForeignKey('insurance.id'))
#     description = db.Column(db.String(300))
#     sum = db.Column(db.String(45))
#     insurance = db.relationship('Insurance', backref='settlements')