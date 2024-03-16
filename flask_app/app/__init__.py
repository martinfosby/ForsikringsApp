from flask import Flask
from flask_app.config import Config


def create_app(config_class=Config):
    app = Flask (__name__)
    app.config.from_object(config_class)

    # extensions init
    from flask_app.app.extensions import db, login_manager, admin
    db.init_app(app)
    login_manager.init_app(app)
    admin.init_app(app)

    # app context work
    with app.app_context():
        db.create_all(bind_key="local") # create local database
        db.reflect(bind_key=None) # get default database by reflection

    # blueprints
    from flask_app.app.blueprints.main import bp as main_bp
    from flask_app.app.blueprints.local import bp as local_bp
    from flask_app.app.blueprints.auth import bp as user_bp
    from flask_app.app.blueprints.insurances import bp as insurance_bp
    from flask_app.app.blueprints.management import bp as management_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(local_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(insurance_bp)
    app.register_blueprint(management_bp)

    return app
