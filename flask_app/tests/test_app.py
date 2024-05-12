from app.models import Customer, Insurance, Settlement
from app.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash
from res import string_resource

def create_user(username, password, is_admin=False):
    hashed_password = generate_password_hash("testpassword")
    # Create a new user instance
    user = Customer(username=username, password_hash=hashed_password, is_admin=is_admin)

    # Add the user to the session
    db.session.add(user)

    # Commit the changes to the database
    db.session.commit()

# Helper function to create a user and log them in
def login_user(client, app):
    with app.app_context():
        create_user("testuser", "testpassword")        
    response = client.post("/login", data={"username": "testuser", "password": "testpassword"}, follow_redirects=True)
    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    return response

def test_home_page_redirect(client):
    response = client.get("/")
    assert response.status_code == 302


def test_register_page_render(client):
    response = client.get("/register")
    assert response.status_code == 200

    assert string_resource("register").encode() in response.data

    assert string_resource("username").encode() in response.data

    assert string_resource("password").encode() in response.data

def test_login_page_render(client):
    response = client.get("/login")
    assert response.status_code == 200

    assert string_resource("login").encode() in response.data

    assert string_resource("username").encode() in response.data

    assert string_resource("password").encode() in response.data

def test_register(client):
    response = client.post("/register", data={"username": "testuser", "password": "testpassword"})

    assert response.status_code == 302



def test_register_valid_form(client, app):
    response = client.post("/register", data={"username": "testuser", "password": "testpassword"}, follow_redirects=True)

    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert string_resource("register_success", username="testuser").encode() in response.data

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
    assert string_resource("login_success", username="testuser").encode() in response.data

    # get the current user from session
    with client.session_transaction() as session:
        assert session['_user_id'] == '1'


def test_login_invalid_password(client, app):
    with app.app_context():
        create_user("testuser", "testpassword")        
    response = client.post("/login", data={"username": "testuser", "password": "wrongpassword"}, follow_redirects=True)

    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert string_resource("invalid_password").encode() in response.data

def test_login_invalid_username(client, app):
    with app.app_context():
        create_user("testuser", "testpassword")        
    response = client.post("/login", data={"username": "wronguser", "password": "wrongpassword"}, follow_redirects=True)

    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert string_resource("invalid_username").encode() in response.data



def test_logout_success(client, app):
    with app.app_context():
        create_user("testuser", "testpassword")        
    response = client.post("/login", data={"username": "testuser", "password": "testpassword"}, follow_redirects=True)
    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert string_resource("login_success", username="testuser").encode() in response.data

    response = client.get("/logout", follow_redirects=True)
    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert string_resource("logout_success", username="testuser").encode() in response.data


def test_make_insurance(client, app):
    with app.app_context():
        create_user("testuser", "testpassword")        
    response = client.post("/login", data={"username": "testuser", "password": "testpassword"}, follow_redirects=True)

    response = client.get("/make/insurance", follow_redirects=True)
    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert string_resource("make_insurance_title").encode() in response.data

    response = client.post("/make/insurance", data={"label": "Test Insurance", "unit_type_id": "1", "value": "575", "price": "33444", "due_date": "2025-01-01", "company_id": "1"}, follow_redirects=True)
    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index

    with app.app_context():
        insurance = Insurance.query.filter_by().first()
    assert insurance
    assert string_resource("make_insurance_success").encode() in response.data

def test_make_offer(client, app):
    with app.app_context():
        create_user("testuser", "testpassword")        
    response = client.post("/login", data={"username": "testuser", "password": "testpassword"}, follow_redirects=True)

    response = client.get("/make/offer", follow_redirects=True)
    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert string_resource("make_offer_title").encode() in response.data

    response = client.post("/make/insurance", data={"label": "Test Insurance", "unit_type_id": "1", "value": "575", "price": "33444", "due_date": "2025-01-01", "company_id": "1"}, follow_redirects=True)

    response = client.post("/make/offer", data={"label": "Test Offer", "price": "100", "company_id": "1", "insurance_id": "1"}, follow_redirects=True)
    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert string_resource("make_offer_success").encode() in response.data


def test_make_settlement(client, app):
    with app.app_context():
        create_user("testuser", "testpassword")        
    response = client.post("/login", data={"username": "testuser", "password": "testpassword"}, follow_redirects=True)
    response = client.post("/make/insurance", data={"label": "Test Insurance", "unit_type_id": "1", "value": "575", "price": "33444", "due_date": "2025-01-01", "company_id": "1"}, follow_redirects=True)

    response = client.get("/make/settlement", follow_redirects=True)
    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert string_resource("make_settlement_title").encode() in response.data

    response = client.post("/make/settlement", data={"insurance_label": "1", "description": "Test Description", "sum": "100"}, follow_redirects=True)
    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert string_resource("make_settlement_success").encode() in response.data

    with app.app_context():
        settlement = Settlement.query.filter_by().first()
    assert settlement

def test_details(client, app):
    with app.app_context():
        create_user("testuser", "testpassword")        
    response = client.post("/login", data={"username": "testuser", "password": "testpassword"}, follow_redirects=True)

    response = client.get("/detail", follow_redirects=True)
    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert string_resource("detail").encode() in response.data


def test_delete(client, app):
    with app.app_context():
        create_user("testuser", "testpassword")        
    response = client.post("/login", data={"username": "testuser", "password": "testpassword"}, follow_redirects=True)

    response = client.get("/delete", follow_redirects=True)
    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert string_resource("delete").encode() in response.data

    response = client.post("/delete", data={"username": "testuser", "password": "testpassword"}, follow_redirects=True)
    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert string_resource("deleted_account", username="testuser").encode() in response.data

    with app.app_context():
        assert not db.session.query(Customer).filter_by(username="testuser").first()


def test_change_password(client, app):
    with app.app_context():
        create_user("testuser", "testpassword")        
    response = client.post("/login", data={"username": "testuser", "password": "testpassword"}, follow_redirects=True)

    response = client.get("/change/password", follow_redirects=True)
    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert string_resource("change_password_title").encode() in response.data

    response = client.post("/change/password", data={"current_password": "testpassword", "new_password": "newpassword"}, follow_redirects=True)
    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert string_resource("password_changed").encode() in response.data

    with app.app_context():
        password_hash=check_password_hash(db.session.query(Customer).filter_by(username="testuser")
                                            .first().password_hash, "newpassword")
        assert password_hash


def test_offers_list(client, app):
    with app.app_context():
        create_user("testuser", "testpassword")        
    response = client.post("/login", data={"username": "testuser", "password": "testpassword"}, follow_redirects=True)

    response = client.get("/offers", follow_redirects=True)
    assert response.status_code == 200  # or assert response.status_code == 302 for redirect to main.index
    assert string_resource("offers_list").encode() in response.data
