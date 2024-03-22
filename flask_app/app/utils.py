from urllib.parse import urljoin, urlparse


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
