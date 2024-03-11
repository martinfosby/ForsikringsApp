from os import name
from flask import Flask, render_template, request, redirect, session,flash,url_for
import secrets
from flask_login import LoginManager
from models.usermodel import UserLogin  
from models.database import Base, db_session
from auth import auth_bp



login_manager = LoginManager()
app = Flask (__name__)
login_manager.init_app(app)
app.secret_key = secrets.token_urlsafe(16)
app.register_blueprint(auth_bp, url_prefix='/auth')

@login_manager.user_loader
def load_user(user_id):
    User = Base.classes.user
    user = db_session.query(User).get(int(user_id))
    if user:
        return UserLogin(user)
    return None




@app.route('/')
def index():
    return render_template('base.html', title='test')


if name == "__main__":
    app.run(debug=True)


