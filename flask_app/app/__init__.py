from flask import Flask
from flask_app.config import ProductionConfig, DevelopmentConfig, TestingConfig
from flask_app.app import models
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
file_handler = RotatingFileHandler("app.log")
formatter = logging.Formatter("%(asctime)s-%(levelname)s-%(message)s")
logger.addHandler(console_handler)
logger.addHandler(file_handler)

console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)


def create_app(config_class=ProductionConfig):
    app = Flask (__name__)
    app.config.from_object(config_class)

    # extensions init
    from flask_app.app.extensions import db, login_manager, admin, csrf
    db.init_app(app)
    login_manager.init_app(app)
    admin.init_app(app)
    csrf.init_app(app)

   # app context work
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            logger.info("Database created successfully.")
        except Exception as e:
            # If reflection fails, it means the database doesn't exist
            logger.critical("Database creation failed. Attempting to reflect database.", exc_info=True)
            # Try to reflect the database schema
            db.reflect()
            logger.info("Database reflection successful.")


    # blueprints
    from flask_app.app.blueprints.main import bp as main_bp
    from flask_app.app.blueprints.auth import bp as user_bp
    from flask_app.app.blueprints.insurances import bp as insurance_bp
    from flask_app.app.blueprints.management import bp as management_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(insurance_bp)
    app.register_blueprint(management_bp)

    return app
