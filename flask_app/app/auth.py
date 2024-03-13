from flask_app.app.models import User
from flask_app.app.extensions import db
from flask_app.app.extensions import login_manager



login_manager.login_view = "user.login"

@login_manager.user_loader
def load_user(user_id):
    user = db.session.query(User).get(int(user_id))
    return user

