from flask_app.app.extensions import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    __tablename__ = "user"
    __table_args__ = {"autoload": True}

    def __init__(self, username, password_hash, is_admin=False):
        self.username = username
        self.password_hash = generate_password_hash(password_hash)
        self.is_admin = is_admin

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class InsuranceCompany(db.Model):
    __tablename__ = "insurance_company"
    __table_args__ = {"autoload": True}


class Contact(db.Model):
    __tablename__ = "contact"
    __table_args__ = {"autoload": True}


class UnitType(db.Model):
    __tablename__ = "unit_type"
    __table_args__ = {"autoload": True}


class Insurance(db.Model):
    __tablename__ = "insurance"
    __table_args__ = {"autoload": True}


class Offer(db.Model):
    __tablename__ = "offer"
    __table_args__ = {"autoload": True}


class Settlement(db.Model):
    __tablename__ = "settlement"
    __table_args__ = {"autoload": True}