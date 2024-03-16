from flask_login import UserMixin
from flask_app.app.extensions import db

mn = __name__ # module name

class CompanyLocal(db.Model):
    __bind_key__ = "local"
    __tablename__ = "company_local"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90))
    contact_local = db.relationship(f'{mn}.ContactLocal', back_populates='company_local')
    insurance_local = db.relationship(f'{mn}.InsuranceLocal', back_populates='company_local')

class ContactLocal(db.Model):
    __bind_key__ = "local"
    __tablename__ = "contact_local"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90))
    phone_number = db.Column(db.String(30))
    email = db.Column(db.String(90))
    company_id = db.Column(db.Integer, db.ForeignKey('company_local.id'))
    company_local = db.relationship(f'{mn}.CompanyLocal', back_populates='contact_local')

class UserLocal(db.Model, UserMixin):
    __bind_key__ = "local"
    __tablename__ = "user_local"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), unique=True)
    password_hash = db.Column(db.String(512))
    is_admin = db.Column(db.Boolean)
    insurance_local = db.relationship(f'{mn}.InsuranceLocal', back_populates='user_local')

class UnitLocal(db.Model):
    __bind_key__ = "local"
    __tablename__ = "unit_local"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90))
    insurance_local = db.relationship(f'{mn}.InsuranceLocal', back_populates='unit_local')
    offer_local = db.relationship(f'{mn}.OfferLocal', back_populates='unit_local')

class InsuranceLocal(db.Model):
    __bind_key__ = "local"
    __tablename__ = "insurance_local"
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(90))
    value = db.Column(db.Integer)
    price = db.Column(db.Integer)
    due_date = db.Column(db.Date)
    unit_id = db.Column(db.Integer, db.ForeignKey('unit_local.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user_local.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company_local.id'))
    unit_local = db.relationship(f'{mn}.UnitLocal', back_populates='insurance_local')
    user_local = db.relationship(f'{mn}.UserLocal', back_populates='insurance_local')
    company_local = db.relationship(f'{mn}.CompanyLocal', back_populates='insurance_local')

class OfferLocal(db.Model):
    __bind_key__ = "local"
    __tablename__ = "offer_local"
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(90))
    price = db.Column(db.Integer)
    unit_id = db.Column(db.Integer, db.ForeignKey('unit_local.id'))
    unit_local = db.relationship(f'{mn}.UnitLocal', back_populates='offer_local')

class SettlementLocal(db.Model):
    __bind_key__ = "local"
    __tablename__ = "settlement_local"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(300))
    sum = db.Column(db.String(45))
    unit_id = db.Column(db.Integer, db.ForeignKey('unit_local.id'))