from app.extensions import db
from flask_login import UserMixin


class Customer(db.Model, UserMixin):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), unique=True)
    password_hash = db.Column(db.String(512))
    is_admin = db.Column(db.Boolean)
    insurance = db.relationship(f'Insurance', back_populates='customer')


class Company(db.Model):
    __tablename__ = "company"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90))
    contact = db.relationship(f'Contact', back_populates='company')
    insurance = db.relationship(f'Insurance', back_populates='company')


class Contact(db.Model):
    __tablename__ = "contact"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90))
    phone_number = db.Column(db.String(30))
    email = db.Column(db.String(90))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    company = db.relationship(f'Company', back_populates='contact')


class UnitType(db.Model):
    __tablename__ = "unit_type"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90))
    insurance = db.relationship(f'Insurance', back_populates='unit_type')
    offer = db.relationship(f'Offer', back_populates='unit_type')


class Insurance(db.Model):
    __tablename__ = "insurance"
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(90))
    value = db.Column(db.Integer)
    price = db.Column(db.Integer)
    due_date = db.Column(db.Date)
    unit_type_id = db.Column(db.Integer, db.ForeignKey('unit_type.id'))
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    unit_type = db.relationship(f'UnitType', back_populates='insurance')
    customer = db.relationship(f'Customer', back_populates='insurance')
    company = db.relationship(f'Company', back_populates='insurance')


class Offer(db.Model):
    __tablename__ = "offer"
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(90))
    price = db.Column(db.Integer)
    unit_type_id = db.Column(db.Integer, db.ForeignKey('unit_type.id'))
    unit_type = db.relationship(f'UnitType', back_populates='offer')


class Settlement(db.Model):
    __tablename__ = "settlement"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(300))
    sum = db.Column(db.String(45))
    unit_type_id = db.Column(db.Integer, db.ForeignKey('unit_type.id'))