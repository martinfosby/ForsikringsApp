from flask_login import UserMixin, login_required, login_user, logout_user, current_user, LoginManager
from insurance_app import app
from insurance_app.models import User

# flask login init
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view("users/login")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
