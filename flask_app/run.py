from flask import g
from flask_login import current_user
from app import create_app
from app.utils import referral

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)