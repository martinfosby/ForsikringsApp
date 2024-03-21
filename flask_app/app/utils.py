from urllib.parse import urljoin, urlparse
import secrets
from flask import session


def url_has_allowed_host_and_scheme(target, host):
    ref_url = urlparse(host)
    parsed_url = urlparse(urljoin(host, target))
    return parsed_url.scheme in ('http', 'https') and ref_url.netloc == parsed_url.netloc


def test_db_connection(db):
    "Note: Use within app_context"
    try:
        # Try connecting to the database
        with db.engine.connect() as connection:
            print("Connected successfully!")
    except Exception as e:
        # If connection fails, print the error
        print("Connection failed:", e)


def generate_csrf_token():
    if 'csrf_token' not in session:
        session['csrf_token'] = secrets.token_hex(16)
    return session['csrf_token']