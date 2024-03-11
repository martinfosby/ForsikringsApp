from werkzeug.security import generate_password_hash, check_password_hash


def set_password(password):
    password_hash = generate_password_hash(password)

def check_password_hash(password_hash, password):
    return check_password_hash(password_hash, password)