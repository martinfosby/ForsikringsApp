from werkzeug.security import generate_password_hash, check_password_hash


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