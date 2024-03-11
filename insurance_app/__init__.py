from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from insurance_app.blueprints.user import user_bp
from insurance_app.blueprints.insurance import insurance_bp
import secrets

# azure server details
server = 'bv-server-mysql.mysql.database.azure.com'  # Your Azure MySQL server name
database = 'myDb'  # Your MySQL database name
username = 'bodovision'  # Your MySQL username
password = 'veldig bra Grupp3'  # Your MySQL password

# connection strings
# Note: No need for specifying the driver when using mysql-connector-python
# sqlite_string = f'sqlite:///project.db'
connection_string = f'mysql+mysqlconnector://{username}:{password}@{server}/{database}'

# app details
app = Flask (__name__)
app.secret_key = secrets.token_urlsafe(16)
app.register_blueprint(user_bp)
app.register_blueprint(insurance_bp)
app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

# sqlalchemy init
db = SQLAlchemy(app)

# Test the connection
with app.app_context():
    try:
        # Try connecting to the database
        with db.engine.connect() as connection:
            print("Connected successfully!")
    except Exception as e:
        # If connection fails, print the error
        print("Connection failed:", e)