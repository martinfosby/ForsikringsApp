from flask_app.app.extensions import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    __tablename__ = "user"
    __table_args__ = {"autoload": True}

    def __init__(self, username, password_hash, is_admin=False):
        self.username = username
        self.password_hash = password_hash
        self.is_admin = is_admin


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