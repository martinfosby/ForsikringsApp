from flask import Flask, render_template, request, redirect, session,flash,url_for
import secrets
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import inspect
from flask_sqlalchemy import SQLAlchemy

# Update these parameters to match your MySQL database details
server = 'bv-server-mysql.mysql.database.azure.com'  # Your Azure MySQL server name
database = 'myDb'  # Your MySQL database name
username = 'bodovision'  # Your MySQL username
password = 'veldig bra Grupp3'  # Your MySQL password

# Note: No need for specifying the driver when using mysql-connector-python
connection_string = f'mysql+mysqlconnector://{username}:{password}@{server}/{database}'

sqllite_string = f'sqlite:///project.db'

app = Flask (__name__)
app.secret_key = secrets.token_urlsafe(16)
# app.config['SQLALCHEMY_DATABASE_URI'] = connection_string
app.config['SQLALCHEMY_DATABASE_URI'] = sqllite_string


db = SQLAlchemy(app)

class InsuranceCompany(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(90))

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('insurance_company.id'))
    name = db.Column(db.String(90))
    phone_number = db.Column(db.String(30))
    email = db.Column(db.String(90))
    company = db.relationship('InsuranceCompany', backref='contacts')

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(45), unique=True)
    password_hash = db.Column(db.String(128))
    is_admin = db.Column(db.Boolean)

class UnitType(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit_name = db.Column(db.String(90))

class Insurance(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(90))
    unit_id = db.Column(db.Integer, db.ForeignKey('unit_type.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    value = db.Column(db.Integer)
    price = db.Column(db.Integer)
    due_date = db.Column(db.Date)
    company_id = db.Column(db.Integer, db.ForeignKey('insurance_company.id'))
    unit_type = db.relationship('UnitType', backref='insurances')
    user = db.relationship('User', backref='insurances')
    company = db.relationship('InsuranceCompany', backref='insurances')

class Offer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    label = db.Column(db.String(90))
    unit_id = db.Column(db.Integer, db.ForeignKey('insurance.id'))
    price = db.Column(db.Integer)
    insurance = db.relationship('Insurance', backref='offers')

class Settlement(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    unit_id = db.Column(db.Integer, db.ForeignKey('insurance.id'))
    description = db.Column(db.String(300))
    sum = db.Column(db.String(45))
    insurance = db.relationship('Insurance', backref='settlements')

@app.route('/')
def index():
    return render_template('base.html', title='test')


@app.route("/users")
def user_list():
    users = db.session.execute(db.select(User).order_by(User.username)).scalars()
    return render_template("user/list.html", users=users)

@app.route("/users/create", methods=["GET", "POST"])
def user_create():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            # email=request.form["email"],
            password_hash=request.form["password"]
        )
        db.session.add(user)
        db.session.commit()
        return redirect(url_for("user_detail", id=user.id))

    return render_template("user/create.html")

# @app.route("/users/login", methods=["GET"])
# def user_login():
#     user = User(
#         username=request.form["username"],
#         # email=request.form["email"],
#         password_hash=request.form["password"]
#     )

#     return render_template("user/create.html")

@app.route("/user/<int:id>")
def user_detail(id):
    user = db.get_or_404(User, id)
    return render_template("user/detail.html", user=user)

@app.route("/user/<int:id>/delete", methods=["GET", "POST"])
def user_delete(id):
    user = db.get_or_404(User, id)

    if request.method == "POST":
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("user_list"))

    return render_template("user/delete.html", user=user)


if __name__ == "__main__":
    with app.app_context():
        db.create_all()

    app.run(debug=True)
