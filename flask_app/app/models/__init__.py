from dataclasses import dataclass
from datetime import date
from app.extensions import db
from flask_login import UserMixin

# Customer Model
class Customer(db.Model, UserMixin):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), unique=True)
    password_hash = db.Column(db.String(512))
    is_admin = db.Column(db.Boolean)
    insurance = db.relationship('Insurance', back_populates='customer')

# Company Model
class Company(db.Model):
    __tablename__ = "company"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90), unique=True)
    contact = db.relationship('Contact', back_populates='company')
    insurance = db.relationship('Insurance', back_populates='company')
    offers = db.relationship("Offer", back_populates="company")

# Contact Model
class Contact(db.Model):
    __tablename__ = "contact"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90))
    phone_number = db.Column(db.String(30))
    email = db.Column(db.String(90))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    company = db.relationship('Company', back_populates='contact')

# UnitType Model
class UnitType(db.Model):
    __tablename__ = "unit_type"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90), unique=True)
    insurance = db.relationship('Insurance', back_populates='unit_type')

@dataclass
class Insurance(db.Model):
    __tablename__ = "insurance"
    id: int = db.Column(db.Integer, primary_key=True)
    label: str = db.Column(db.String(90), nullable=True)
    value: int = db.Column(db.Integer, nullable=True)
    price: int = db.Column(db.Integer, nullable=True)
    due_date: str = db.Column(db.Date, nullable=True)
    unit_type_id: int = db.Column(db.Integer, db.ForeignKey('unit_type.id'))
    customer_id: int = db.Column(db.Integer, db.ForeignKey('customer.id'))
    company_id: int = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)
    unit_type = db.relationship('UnitType', back_populates='insurance')
    customer = db.relationship('Customer', back_populates='insurance')
    company = db.relationship('Company', back_populates='insurance')
    settlement = db.relationship('Settlement', back_populates='insurance')
    offers = db.relationship("Offer", back_populates="insurance")

    def to_dict(self):
        return {
            'id': self.id,
            'label': self.label,
            'value': self.value,
            'price': self.price,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'unit_type_id': self.unit_type_id,
            'customer_id': self.customer_id,
            'company_id': self.company_id,
        }

# Offer Model
class Offer(db.Model):
    __tablename__ = "offer"
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(90))
    price = db.Column(db.Integer)
    insurance_id = db.Column(db.Integer, db.ForeignKey('insurance.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))

    insurance = db.relationship("Insurance", back_populates="offers")
    company = db.relationship("Company", back_populates="offers")

# Settlement Model
class Settlement(db.Model):
    __tablename__ = "settlement"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(300))
    sum = db.Column(db.String(45))
    insurance_id = db.Column(db.Integer, db.ForeignKey('insurance.id'))
    insurance = db.relationship('Insurance', back_populates='settlement')