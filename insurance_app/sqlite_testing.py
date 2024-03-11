from insurance_app import app, db
from flask import Flask, render_template, request, redirect, session,flash,url_for
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import inspect
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_required, login_user, logout_user, current_user, LoginManager
from werkzeug.security import generate_password_hash, check_password_hash


# user tables 
class InsuranceCompany(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90))


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('insurance_company.id'))
    name = db.Column(db.String(90))
    phone_number = db.Column(db.String(30))
    email = db.Column(db.String(90))
    company = db.relationship('InsuranceCompany', backref='contacts')


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class UnitType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit_name = db.Column(db.String(90))


class Insurance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(90))
    unit_id = db.Column(db.Integer, db.ForeignKey('unit_type.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    value = db.Column(db.Integer)
    price = db.Column(db.Integer)
    due_date = db.Column(db.Date)
    company_id = db.Column(db.Integer, db.ForeignKey('insurance_company.id'))
    unit_type = db.relationship('UnitType', backref='insurances')
    user = db.relationship('User', backref='insurances')
    company = db.relationship('InsuranceCompany', backref='insurances')


class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(90))
    unit_id = db.Column(db.Integer, db.ForeignKey('insurance.id'))
    price = db.Column(db.Integer)
    insurance = db.relationship('Insurance', backref='offers')


class Settlement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('insurance.id'))
    description = db.Column(db.String(300))
    sum = db.Column(db.String(45))
    insurance = db.relationship('Insurance', backref='settlements')