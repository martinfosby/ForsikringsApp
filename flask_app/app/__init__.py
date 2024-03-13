from flask import Flask
from flask_app.app.utils import test_db_connection
from flask_app.config import Config
from flask_app.app.extensions import db, login_manager


def create_app(config_class=Config):
    app = Flask (__name__)
    app.config.from_object(config_class)

    # extensions init
    db.init_app(app)
    login_manager.init_app(app)

    # app context work
    with app.app_context():
        test_db_connection(db) 
        db.reflect() # get database by reflection

    # blueprints
    from flask_app.app.blueprints.main import bp as main_bp
    from flask_app.app.blueprints.auth import bp as user_bp
    from flask_app.app.blueprints.insurance import bp as insurance_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(insurance_bp)

    return app
