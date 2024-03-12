from sqlalchemy import false
from insurance_app import app
from insurance_app.models import *
from insurance_app.utils import set_password, check_password_hash
from flask import Flask, render_template, request, redirect, session,flash,url_for
from flask_login import login_required, login_user, logout_user, current_user, LoginManager

@app.route('/')
def index():
    return render_template('base.html', title='test')

