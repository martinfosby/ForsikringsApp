from flask import abort, render_template, request, redirect, session,flash,url_for
from flask_login import login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_app.app.extensions import db, login_manager
from flask_app.app.models import User
from flask_app.app.blueprints.auth import bp
from flask_app.app.blueprints.auth.forms.register_form import RegisterForm
from flask_app.app.blueprints.auth.forms.login_form import LoginForm
from flask_app.app.blueprints.auth.login_manager import load_user

@bp.route("/users")
def list():
    users = db.session.execute(db.select(User).order_by(User.username)).scalars()
    return render_template("auth/list.html", users=users)


@bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Process form data and create user
        username = form.username.data
        password = form.password.data

        password_hash = generate_password_hash(password)
        # Creating the new user with the hashed password
        user = User(
            username=username,
            password_hash=password_hash,
            is_admin=False
        )
        
        # Adding and committing the user to the database
        db.session.add(user)
        db.session.commit()

        login_user(user)

        return redirect(url_for('main.index')) 

    # Render the user creation form for GET requests
    return render_template("auth/register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        next = request.form.get('next')
        user = db.session.query(User).filter_by(username=username).first()
        # Check if the user exists and the password is correct
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Logged in successfully.')
            # url_has_allowed_host_and_scheme should check if the url is safe
            # for redirects, meaning it matches the request host.
            # See Django's url_has_allowed_host_and_scheme for an example.
            # if not url_has_allowed_host_and_scheme(request.host_url, next):
            #     return abort(400)

            return redirect(next or url_for('main.index'))
        else:
            flash('Invalid username or password')
            return redirect(url_for(".login"))

    return render_template('auth/login.html', form=form)


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@bp.route("/user/<int:id>")
@login_required
def detail(id):
    user = db.get_or_404(User, id)
    if current_user == user:
        return render_template("auth/detail.html", user=user)
    else:
        return redirect(url_for(".login"))


@bp.route("/user/<int:id>/delete", methods=["GET", "POST"])
@login_required
def delete(id):
    user = db.get_or_404(User, id)

    if request.method == "POST":
        db.session.delete(user)
        db.session.commit()
        return redirect(url_for(".user_list"))

    return render_template("auth/delete.html", user=user)


@bp.route("/user-by-id/<int:id>")
def user_by_id(id):
    user = db.get_or_404(User, id)
    return render_template("show_user.html", user=user)

@bp.route("/user-by-username/<username>")
def user_by_username(username):
    user = db.one_or_404(
        db.select(User).filter_by(username=username),
        description=f"No user named '{username}'."
    )
    return render_template("show_user.html", user=user)

