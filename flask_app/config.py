import os
import secrets
from dotenv import load_dotenv

load_dotenv(override=True)

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Unit testing
    TESTING = False
    # App config
    SECRET_KEY = secrets.token_urlsafe(16)
    # sqlalchemy config
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True  # Enable echoing of SQL statements
    # flask-login config
    USE_SESSION_FOR_NEXT = True


class ProductionConfig(Config):
    """Uses production database server."""
     # Azure server details
    DB_SERVER = os.getenv("DB_SERVER") # Your Azure MySQL server name
    DATABASE = os.getenv("DATABASE")  # Your MySQL database name
    USERNAME = os.getenv("USERNAME")# Your MySQL username
    PASSWORD = os.getenv("PASSWORD")  # Your MySQL password
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{DB_SERVER}/{DATABASE}'


class DevelopmentConfig(Config):
    """Uses development database server."""
    DB_SERVER = 'localhost'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///sandbox.db'


class TestingConfig(Config):
    """Uses in-memory database server for unit testing."""
    DB_SERVER = 'localhost'
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    TESTING = True
    WTF_CSRF_ENABLED = False

