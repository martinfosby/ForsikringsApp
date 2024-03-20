from flask_app.app.extensions import db
from flask_login import UserMixin

mn = __name__ # module name


class Customer(db.Model, UserMixin):
    __tablename__ = "customer"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), unique=True)
    password_hash = db.Column(db.String(512))
    is_admin = db.Column(db.Boolean)
    insurance = db.relationship(f'{mn}.Insurance', back_populates='customer')


class Company(db.Model):
    __tablename__ = "company"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90))
    contact = db.relationship(f'{mn}.Contact', back_populates='company')
    insurance = db.relationship(f'{mn}.Insurance', back_populates='company')


class Contact(db.Model):
    __tablename__ = "contact"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90))
    phone_number = db.Column(db.String(30))
    email = db.Column(db.String(90))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    company = db.relationship(f'{mn}.Company', back_populates='contact')


class Category(db.Model):
    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90))
    insurance = db.relationship(f'{mn}.Insurance', back_populates='category')
    offer = db.relationship(f'{mn}.Offer', back_populates='category')


class Insurance(db.Model):
    __tablename__ = "insurance"
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(90))
    value = db.Column(db.Integer)
    price = db.Column(db.Integer)
    due_date = db.Column(db.Date)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('customer.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('company.id'))
    category = db.relationship(f'{mn}.Category', back_populates='insurance')
    customer = db.relationship(f'{mn}.Customer', back_populates='insurance')
    company = db.relationship(f'{mn}.Company', back_populates='insurance')


class Offer(db.Model):
    __tablename__ = "offer"
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(90))
    price = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship(f'{mn}.Category', back_populates='offer')


class Settlement(db.Model):
    __tablename__ = "settlement"
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(300))
    sum = db.Column(db.String(45))
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))