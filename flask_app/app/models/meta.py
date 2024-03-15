from flask_login import UserMixin
from flask_app.app.extensions import db


class CompanyMeta(db.Model):
    __tablename__ = "company"
    __bind_key__ = "meta"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90))
    contact = db.relationship('ContactMeta', back_populates='company')
    insurance = db.relationship('InsuranceMeta', back_populates='company')

class ContactMeta(db.Model):
    __tablename__ = "contact"
    __bind_key__ = "meta"
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    name = db.Column(db.String(90))
    phone_number = db.Column(db.String(30))
    email = db.Column(db.String(90))
    company = db.relationship('CompanyMeta', back_populates='contact')

class UserMeta(db.Model, UserMixin):
    __tablename__ = "user"
    __bind_key__ = "meta"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), unique=True)
    password_hash = db.Column(db.String(512))
    is_admin = db.Column(db.Boolean)
    insurance = db.relationship('InsuranceMeta', back_populates='user')

class UnitMeta(db.Model):
    __tablename__ = "unit"
    __bind_key__ = "meta"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90))
    insurance = db.relationship('InsuranceMeta', back_populates='unit')

class InsuranceMeta(db.Model):
    __tablename__ = "insurance"
    __bind_key__ = "meta"
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(90))
    value = db.Column(db.Integer)
    price = db.Column(db.Integer)
    due_date = db.Column(db.Date)
    unit_id = db.Column(db.Integer, db.ForeignKey('unit.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    unit = db.relationship('UnitMeta', back_populates='insurance')
    user = db.relationship('UserMeta', back_populates='insurance')
    company = db.relationship('CompanyMeta', back_populates='insurance')
    offer = db.relationship('OfferMeta', back_populates='insurance')
    settlement = db.relationship('SettlementMeta', back_populates='insurance')

class OfferMeta(db.Model):
    __tablename__ = "offer"
    __bind_key__ = "meta"
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(90))
    unit_id = db.Column(db.Integer, db.ForeignKey('insurance.id'))
    price = db.Column(db.Integer)
    insurance = db.relationship('InsuranceMeta', back_populates='offer')

class SettlementMeta(db.Model):
    __tablename__ = "settlement"
    __bind_key__ = "meta"
    id = db.Column(db.Integer, primary_key=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('insurance.id'))
    description = db.Column(db.String(300))
    sum = db.Column(db.String(45))
    insurance = db.relationship('InsuranceMeta', back_populates='settlement')