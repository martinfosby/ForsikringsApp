from dataclasses import dataclass
from datetime import date
from app.extensions import db
from flask_login import UserMixin
from sqlalchemy.ext import serializer

class CompanyLocal(db.Model):
    __tablename__ = "company"
    __bind_key__ = "local"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90))
    # contact = db.relationship(f'Contact', back_populates='company')
    insurance = db.relationship(f'InsuranceLocal', back_populates='company')

@dataclass()
class InsuranceLocal(db.Model):
    __tablename__ = "insurance"
    __bind_key__ = "local"
    id: int = db.Column(db.Integer, primary_key=True)
    label: str = db.Column(db.String(90), nullable=True)
    value: int = db.Column(db.Integer, nullable=True)
    price: int = db.Column(db.Integer, nullable=True)
    due_date: str = db.Column(db.Date, nullable=True)
    # company: str = db.Column(db.String(90), nullable=True)
    unit_type_id: int = db.Column(db.Integer, db.ForeignKey('unit_type.id'))
    # customer_id: int = db.Column(db.Integer, db.ForeignKey('customer.id'))
    company_id: int = db.Column(db.Integer, db.ForeignKey('company.id'), nullable=True)
    unit_type = db.relationship(f'UnitTypeLocal', back_populates='insurance')
    # customer = db.relationship(f'Customer', back_populates='insurance')
    company = db.relationship(f'CompanyLocal', back_populates='insurance')
    settlement = db.relationship(f'SettlementLocal', back_populates='insurance')

    def to_dict(self):
        return {
            'id': self.id,
            'label': self.label,
            'value': self.value,
            'price': self.price,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'unit_type_id': self.unit_type_id,
            # 'customer_id': self.customer_id,
            'company_id': self.company_id,
        }


class UnitTypeLocal(db.Model):
    __tablename__ = "unit_type"
    __bind_key__ = "local"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90))
    insurance = db.relationship(f'InsuranceLocal', back_populates='unit_type')
    offer = db.relationship(f'OfferLocal', back_populates='unit_type')


class OfferLocal(db.Model):
    __tablename__ = "offer"
    __bind_key__ = "local"

    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(90))
    price = db.Column(db.Integer)
    unit_type_id = db.Column(db.Integer, db.ForeignKey('unit_type.id'))
    unit_type = db.relationship(f'UnitTypeLocal', back_populates='offer')


class SettlementLocal(db.Model):
    __tablename__ = "settlement"
    __bind_key__ = "local"

    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(300))
    sum = db.Column(db.String(45))
    insurance_id = db.Column(db.Integer, db.ForeignKey('insurance.id'))
    insurance = db.relationship(f'InsuranceLocal', back_populates='settlement')
