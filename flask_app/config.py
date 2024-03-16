import os
import secrets
from dotenv import load_dotenv

load_dotenv()

basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Azure server details
    # SERVER = os.getenv("SERVER") # Your Azure MySQL server name
    # DATABASE = os.getenv("DATABASE")  # Your MySQL database name
    # USERNAME = os.getenv("USERNAME")# Your MySQL username
    # PASSWORD = os.getenv("PASSWORD")  # Your MySQL password
    SERVER="bv-server-mysql.mysql.database.azure.com"  # Your Azure MySQL server name
    DATABASE="myDb"  # Your MySQL database name
    USERNAME="bodovision"  # Your MySQL username
    PASSWORD="veldig bra Grupp3"  # Your MySQL password

    # App config
    # NAME = 'Insurance'
    SECRET_KEY = secrets.token_urlsafe(16)
    # sqlalchemy config
    SQLALCHEMY_DATABASE_URI = f'mysql+mysqlconnector://{USERNAME}:{PASSWORD}@{SERVER}/{DATABASE}'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_ECHO = True  # Enable echoing of SQL statements
    # flask-login config
    USE_SESSION_FOR_NEXT = True




