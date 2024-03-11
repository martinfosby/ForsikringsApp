from insurance_app import app
from insurance_app.database import db, User, InsuranceCompany
from insurance_app.utils import set_password, check_password_hash
from flask import Flask, render_template, request, redirect, session,flash,url_for
from flask_login import login_required, login_user, logout_user, current_user, LoginManager

@app.route('/')
def index():
    return render_template('base.html', title='test')


@app.route("/users")
def user_list():
    users = db.session.execute(db.select(User).order_by(User.username)).scalars()
    return render_template("list.html", users=users)
