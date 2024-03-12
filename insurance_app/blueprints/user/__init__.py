from flask import Blueprint, render_template, request, redirect, session,flash,url_for
from flask_login import login_required, login_user, logout_user, current_user, LoginManager
from insurance_app.models import db, User
from insurance_app.utils import set_password, check_password_hash

user_bp = Blueprint("user", __name__, static_folder="static", template_folder="templates")


@user_bp.route("/users")
def list():
    users = db.session.execute(db.select(User).order_by(User.username)).scalars()
    return render_template("list.html", users=users)


@user_bp.route("/users/create", methods=["GET", "POST"])
def create():
    if request.method == "POST":
        # Generating the password hash
        password_hash = set_password((request.form["password"]))

        # Creating the new user with the hashed password
        user = User(
            username=request.form["username"],
            # email=request.form["email"],
            password_hash=password_hash,
            is_admin=False
        )
        
        # Adding and committing the user to the database
        db.session.add(user)
        db.session.commit()

        # Redirecting to the user detail page after creation
        return redirect(url_for("detail", id=user.id))

    # Render the user creation form for GET requests
    return render_template("create.html")


@user_bp.route("/users/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Retrieve the user from the database based on the provided username
        user = User.query.filter_by(username=username).first()

        # Check if the user exists and the password is correct
        if user and check_password_hash(user.password_hash, password):
            login_user(user)  # Log in the user
            return redirect(url_for("user_detail", id=user.id))
        else:
            # You may want to handle invalid login attempts, for example, by rendering an error message
            return render_template("login.html", error="Invalid username or password")

    return render_template("login.html")


@user_bp.route("/user/<int:id>")
@login_required
def detail(id):
    user = db.get_or_404(User, id)
    return render_template("detail.html", user=user)


@user_bp.route("/user/<int:id>/delete", methods=["GET", "POST"])
@login_required
def delete(id):
    user = db.get_or_404(User, id)

    if request.method == "POST":
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for("user_list"))

    return render_template("delete.html", user=user)