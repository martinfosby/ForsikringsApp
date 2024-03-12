from flask_app.app.models import User
from flask_app.app.extensions import login_manager



login_manager.login_view = "user.login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

