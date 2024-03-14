from flask_login import UserMixin
from flask_app.app.extensions import db


# class InsuranceCompanyMeta(db.Model):
#     __bind_key__ = "meta"
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(90))

# class ContactMeta(db.Model):
#     __bind_key__ = "meta"
#     id = db.Column(db.Integer, primary_key=True)
#     company_id = db.Column(db.Integer, db.ForeignKey('insurance_company.id'))
#     name = db.Column(db.String(90))
#     phone_number = db.Column(db.String(30))
#     email = db.Column(db.String(90))
#     company = db.relationship('InsuranceCompanyMeta', backref='contacts')

class UserMeta(db.Model, UserMixin):
    __bind_key__ = "meta"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean)

# class UnitTypeMeta(db.Model):
#     __bind_key__ = "meta"
#     id = db.Column(db.Integer, primary_key=True)
#     unit_name = db.Column(db.String(90))

# class InsuranceMeta(db.Model):
#     __bind_key__ = "meta"
#     id = db.Column(db.Integer, primary_key=True)
#     label = db.Column(db.String(90))
#     unit_id = db.Column(db.Integer, db.ForeignKey('unit_type.id'))
#     user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
#     value = db.Column(db.Integer)
#     price = db.Column(db.Integer)
#     due_date = db.Column(db.Date)
#     company_id = db.Column(db.Integer, db.ForeignKey('insurance_company.id'))
#     unit_type = db.relationship('UnitType', backref='insurances')
#     user = db.relationship('User', backref='insurances')
#     company = db.relationship('InsuranceCompanyMeta', backref='insurances')

# class OfferMeta(db.Model):
#     __bind_key__ = "meta"
#     id = db.Column(db.Integer, primary_key=True)
#     label = db.Column(db.String(90))
#     unit_id = db.Column(db.Integer, db.ForeignKey('insurance.id'))
#     price = db.Column(db.Integer)
#     insurance = db.relationship('InsuranceMeta', backref='offers')

# class SettlementMeta(db.Model):
#     __bind_key__ = "meta"
#     id = db.Column(db.Integer, primary_key=True)
#     unit_id = db.Column(db.Integer, db.ForeignKey('insurance.id'))
#     description = db.Column(db.String(300))
#     sum = db.Column(db.String(45))
#     insurance = db.relationship('InsuranceMeta', backref='settlements')