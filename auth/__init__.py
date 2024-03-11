from flask import render_template, redirect, url_for, flash, Blueprint
from .forms import LoginForm
from flask_login import login_user,current_user
from models.usermodel import UserLogin
from models.database import Base, db_session

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login_view():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        User = Base.classes.user
        user = db_session.query(User).filter_by(username=username).first()
        if user and user.password_hash == password:
            user_login = UserLogin(user)
            login_user(user_login)
            #return redirect(url_for('main.index')) 
            return("Logged in successfully!")
        else:
            flash('Invalid username or password')
    return render_template('login.html', form=form)