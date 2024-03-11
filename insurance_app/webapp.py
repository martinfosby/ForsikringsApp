from insurance_app import app
from insurance_app import views


if __name__ == "__main__":
    with app.app_context():
        app.run(debug=True)