from flask import Flask
from flask_app.config import Config
from flask_app.app.extensions import db, login_manager


def create_app(config_class=Config):
    app = Flask (__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    # Test the connection
    with app.app_context():
        # blueprints
        from flask_app.app.blueprints.main import bp as main_bp
        from flask_app.app.blueprints.user import bp as user_bp
        from flask_app.app.blueprints.insurance import bp as insurance_bp
        login_manager.init_app(app)
        app.register_blueprint(main_bp, url_prefix="")
        app.register_blueprint(user_bp, url_prefix="")
        app.register_blueprint(insurance_bp, url_prefix="")



    return app
