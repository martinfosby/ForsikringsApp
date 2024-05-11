from sys import exc_info
from flask import session
import pytest
from sqlalchemy.exc import IntegrityError
from app.models import Customer
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

def create_user(username, password, is_admin=False):
    hashed_password = generate_password_hash("testpassword")
    # Create a new user instance
    user = Customer(username=username, password_hash=hashed_password, is_admin=is_admin)

    # Add the user to the session
    db.session.add(user)

    # Commit the changes to the database
    db.session.commit()

def test_home_page_redirect(client):
    response = client.get("/")
    assert response.status_code == 302


def test_register_page_render(client):
    response = client.get("/register")
    assert response.status_code == 200

    assert b"Register" in response.data

    assert b"Username" in response.data

    assert b"Password" in response.data

def test_login_page_render(client):
    response = client.get("/login")
    assert response.status_code == 200

    assert b"Login" in response.data

    assert b"Username" in response.data

    assert b"Password" in response.data

def test_register(client):
    response = client.post("/register", data={"username": "testuser", "password": "testpassword"})

    assert response.status_code == 302



def test_register_valid_form(client, app):
    response = client.post("/register", data={"username": "testuser", "password": "testpassword"}, follow_redirects=True)

    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert b"User testuser created" in response.data

    # Optionally, assert that the user exists in the database
    with app.app_context():
        user = Customer.query.filter_by(username="testuser").first()
    assert user is not None
    

def test_register_existing_user(client, app):
    # Create a test user
    hashed_password = generate_password_hash("testpassword")
    user = Customer(username="testuser", password_hash=hashed_password, is_admin=False)
    with app.app_context():
        users_count = Customer.query.filter_by(username="testuser").count() # check if users is empty at the beginning
        db.session.add(user)
        db.session.commit()
    assert users_count == 0

    # Attempt to register the same user again
    response = client.post("/register", data={"username": "testuser", "password": "testpassword"}, follow_redirects=True)
    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to register

    # Optionally, assert that the user is not logged in after registration attempt

    # Optionally, assert that no additional user was added to the database
    with app.app_context():
        users_count = Customer.query.filter_by(username="testuser").count()
    assert users_count == 1



def test_login_valid_form(client, app):
    with app.app_context():
        create_user("testuser", "testpassword")        
    response = client.post("/login", data={"username": "testuser", "password": "testpassword"}, follow_redirects=True)

    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert b"Logged in successfully as testuser" in response.data

    # get the current user from session
    with client.session_transaction() as session:
        assert session['_user_id'] == '1'


def test_login_invalid_password(client, app):
    with app.app_context():
        create_user("testuser", "testpassword")        
    response = client.post("/login", data={"username": "testuser", "password": "wrongpassword"}, follow_redirects=True)

    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert b"Invalid password" in response.data

def test_login_invalid_username(client, app):
    with app.app_context():
        create_user("testuser", "testpassword")        
    response = client.post("/login", data={"username": "wronguser", "password": "wrongpassword"}, follow_redirects=True)

    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert b"Invalid username" in response.data



def test_logout(client, app):
    with app.app_context():
        create_user("testuser", "testpassword")        
    response = client.post("/login", data={"username": "testuser", "password": "testpassword"}, follow_redirects=True)
    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert b"Logged in successfully as testuser" in response.data

    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert b"Logged out successfully" in response.data


def test_make_insurance(client, app):
    with app.app_context():
        create_user("testuser", "testpassword")        
    response = client.post("/login", data={"username": "testuser", "password": "testpassword"}, follow_redirects=True)
    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert b"Logged in successfully as testuser" in response.data

    response = client.get("/make/insurance", follow_redirects=True)
    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert b"Register Offer" in response.data

    response = client.post("/make/insurance", data={"label": "Test Offer", "price": "100", "company_id": "1", "insurance_id": "1"}, follow_redirects=True)
    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert b"Insurance created" in response.data

def test_make_offer(client, app):
    with app.app_context():
        create_user("testuser", "testpassword")        
    response = client.post("/login", data={"username": "testuser", "password": "testpassword"}, follow_redirects=True)
    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert b"Logged in successfully as testuser" in response.data

    response = client.get("/make/offer", follow_redirects=True)
    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert b"Register Offer" in response.data

    response = client.post("/make/offer", data={"label": "Test Offer", "price": "100", "company_id": "1", "insurance_id": "1"}, follow_redirects=True)
    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert b"Offer created" in response.data

def test_details(client, app):
    with app.app_context():
        create_user("testuser", "testpassword")        
    response = client.post("/login", data={"username": "testuser", "password": "testpassword"}, follow_redirects=True)
    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert b"Logged in successfully as testuser" in response.data

    response = client.get("/detail", follow_redirects=True)
    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert b"Detail" in response.data


def test_delete(client, app):
    with app.app_context():
        create_user("testuser", "testpassword")        
    response = client.post("/login", data={"username": "testuser", "password": "testpassword"}, follow_redirects=True)
    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert b"Logged in successfully as testuser" in response.data

    response = client.get("/delete", follow_redirects=True)
    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert b"Delete" in response.data

    response = client.post("/delete", data={"username": "testuser", "password": "testpassword"}, follow_redirects=True)
    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert b"Deleted account testuser" in response.data

    with app.app_context():
        assert not db.session.query(Customer).filter_by(username="testuser").first()


def test_change_password(client, app):
    with app.app_context():
        create_user("testuser", "testpassword")        
    response = client.post("/login", data={"username": "testuser", "password": "testpassword"}, follow_redirects=True)
    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert b"Logged in successfully as testuser" in response.data

    response = client.get("/change/password", follow_redirects=True)
    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert b"Change password" in response.data

    response = client.post("/change/password", data={"current_password": "testpassword", "new_password": "newpassword"}, follow_redirects=True)
    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert b"Password changed successfully" in response.data

    with app.app_context():
        password_hash=check_password_hash(db.session.query(Customer).filter_by(username="testuser")
                                            .first().password_hash, "newpassword")
        assert password_hash


def test_offers_list(client, app):
    with app.app_context():
        create_user("testuser", "testpassword")        
    response = client.post("/login", data={"username": "testuser", "password": "testpassword"}, follow_redirects=True)
    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert b"Logged in successfully as testuser" in response.data

    response = client.get("/offers", follow_redirects=True)
    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert b"Offers" in response.data
