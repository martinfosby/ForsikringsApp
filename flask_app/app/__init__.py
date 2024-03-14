from flask import Flask
from flask_app.config import Config


def create_app(config_class=Config):
    app = Flask (__name__)
    app.config.from_object(config_class)

    # extensions init
    from flask_app.app.extensions import db, login_manager
    db.init_app(app)
    # mdb.init_app(app)
    login_manager.init_app(app)

    # app context work
    with app.app_context():
        db.reflect() # get database by reflection
        # mdb.create_all()

    # blueprints
    from flask_app.app.blueprints.main import bp as main_bp
    from flask_app.app.blueprints.auth import bp as user_bp
    from flask_app.app.blueprints.insurance import bp as insurance_bp
    app.register_blueprint(main_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(insurance_bp)

    return app
