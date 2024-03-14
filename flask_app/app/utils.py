from werkzeug.security import generate_password_hash, check_password_hash
from urllib.parse import urlparse

def url_has_allowed_host_and_scheme(host, next):
    parsed_url = urlparse(host)
    if parsed_url.scheme in ('http', 'https', '') and parsed_url.path == next:
        return True
    else:
        return False


def test_db_connection(db):
    "Note: Use within app_context"
    try:
        # Try connecting to the database
        with db.engine.connect() as connection:
            print("Connected successfully!")
    except Exception as e:
        # If connection fails, print the error
        print("Connection failed:", e)

def set_password(password):
    password_hash = generate_password_hash(password)
    return password_hash

def check_password(password_hash, password):
    return check_password_hash(password_hash, password)