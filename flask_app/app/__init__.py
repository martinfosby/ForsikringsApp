from flask import Flask
from config import ProductionConfig, DevelopmentConfig

def create_app(config_class=ProductionConfig):
    app = Flask (__name__)
    app.config.from_object(config_class)

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
        except Exception as e:
            # If reflection fails, it means the database doesn't exist
            app.logger.critical("Database creation failed. Attempting to reflect database.", exc_info=True)
            # Try to reflect the database schema
            db.reflect()
            app.logger.info("Database reflection successful.")


    # blueprints
    from app.blueprints.main import bp as main_bp
    from app.blueprints.auth import bp as user_bp
    from app.blueprints.insurances import bp as insurance_bp
    from app.blueprints.settlements import bp as settlement_bp
    from app.blueprints.administrator import bp as administrator_bp
    from app.blueprints.api import bp as api_bp
    from app.blueprints.offers import bp as offers_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(insurance_bp)
    app.register_blueprint(settlement_bp)
    app.register_blueprint(administrator_bp)
    app.register_blueprint(api_bp)
    app.register_blueprint(offers_bp)
    
    return app

