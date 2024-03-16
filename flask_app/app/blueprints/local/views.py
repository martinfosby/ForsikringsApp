from flask import redirect, render_template, session, url_for, current_app, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_app.app.extensions import db
from flask_login import login_user
from flask_app.app.blueprints.auth.login_manager import load_user
from flask_app.app.blueprints.auth.forms.register_form import RegisterForm
from flask_app.app.blueprints.auth.forms.login_form import LoginForm
from . import bp
from flask_app.app.localdb import UserLocal



@bp.route("/local/users")
def list():
    users = db.session.execute(db.select(UserLocal).order_by(UserLocal.username)).scalars()
    return render_template("auth/list.html", users=users)

@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        next = request.form.get('next')
        user = db.session.query(UserLocal).filter_by(username=username).first()
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


@bp.route("/local/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Process form data and create user
        username = form.username.data
        password = form.password.data

        password_hash = generate_password_hash(password)
        # Creating the new user with the hashed password
        user = UserLocal(
            username=username,
            password_hash=password_hash,
            is_admin=False
        )
        
        # Adding and committing the user to the database
        db.session.add(user)
        db.session.commit()

        login_user(user)

        return redirect(url_for('local.list'))
        # return redirect(url_for('main.index')) 

    # Render the user creation form for GET requests
    return render_template("auth/register.html", form=form)