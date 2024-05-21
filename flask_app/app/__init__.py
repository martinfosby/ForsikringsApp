from flask import Flask
from config import ProductionConfig, DevelopmentConfig, TestingConfig
from sqlalchemy.exc import ProgrammingError

from app.utils import test_db_connection

def create_app(config_class=ProductionConfig):
    app = Flask (__name__)
    app.config.from_object(config_class)
    # logging user config
    app.logger.info(f"DB_SERVER: {config_class.DB_SERVER}")
    app.logger.info(f"DATABASE: {config_class.DATABASE}")
    app.logger.info(f"USERNAME: {config_class.USERNAME}")
    # extensions init
    from app.extensions import db, login_manager, admin, csrf
    db.init_app(app)
    login_manager.init_app(app)
    admin.init_app(app)
    csrf.init_app(app)

   # app context work
    with app.app_context():
        try:
            # Create all tables
            from app import models # ikke fjern
            db.create_all()
            
            app.logger.info("Database created successfully.")
        except ProgrammingError as pe:
            # configuration error
            app.logger.critical(pe, exc_info=True)
            raise pe
        except Exception as e:
            # If reflection fails, it means the database doesn't exist
            app.logger.critical("Database creation failed. Attempting to reflect database.", exc_info=True)
            # Try to reflect the database schema
            db.reflect()
            app.logger.info("Database reflection successful.")
        
        if config_class == DevelopmentConfig or config_class == TestingConfig:
            from app.models.data import add_data
            add_data()

    # blueprints
    from app.blueprints.main import bp as main_bp
    from app.blueprints.auth import bp as user_bp
    from app.blueprints.insurances import bp as insurance_bp
    from app.blueprints.settlements import bp as settlement_bp
    from app.blueprints.administrator import bp as administrator_bp
    from app.blueprints.api import bp as api_bp
    from app.blueprints.offers import bp as offers_bp
    from app.blueprints.companies import bp as companies_bp
    from app.blueprints.contacts import bp as contacts_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(insurance_bp)
    app.register_blueprint(settlement_bp)
    app.register_blueprint(administrator_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(offers_bp)
    app.register_blueprint(companies_bp)
    app.register_blueprint(contacts_bp)
    
    return app

