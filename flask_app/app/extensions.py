from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from flask_wtf import CSRFProtect

db = SQLAlchemy()
login_manager = LoginManager()
admin = Admin()
csrf = CSRFProtect()