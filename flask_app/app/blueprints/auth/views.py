from flask import abort, render_template, request, redirect, session, flash,url_for, current_app
from flask_login import fresh_login_required, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.utils import url_has_allowed_host_and_scheme
from app.extensions import db, login_manager
from app.models import Customer
from app.blueprints.auth import bp
from app.blueprints.auth.forms.register_form import RegisterForm
from app.blueprints.auth.forms.login_form import LoginForm
from app.blueprints.auth.forms.delete_form import DeleteForm
from .forms.change_password_form import ChangePasswordForm
from .forms.change_username_form import ChangeUsernameForm
from app.blueprints.auth.login_manager import load_user
from sqlalchemy.exc import IntegrityError


@bp.route("/users")
def list():
    # Query the database for all users
    user = current_user
    if not user.is_admin:
        abort(403)
    users = db.session.execute(db.select(Customer).order_by(Customer.username)).scalars()
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
        user = Customer(
            username=username,
            password_hash=password_hash,
            is_admin=False
        )
        
        # try adding and committing the user to the database
        try:
            db.session.add(user)
            db.session.commit()
            current_app.logger.info(f"User {username} created")
            login_user(user)
            flash(f"User {user.username} created", category="success")
        except IntegrityError as ie:
            db.session.rollback()
            mysql_error_code = ie.orig.args[0]
            if mysql_error_code == 1062:  # MySQL error code for duplicate entry
                flash(f"User {user.username} already exists", category="danger")
                current_app.logger.error(f"User {username} already exists {ie}")
            else:
                flash("An error occurred while processing the request", category="danger")
                current_app.logger.error(f"Error creating user: {ie}")
            return redirect(url_for(".register"))
        except Exception as e:
            flash(f"Error creating user: {e}", category="danger")
            current_app.logger.error(f"Error creating user: {e}")
            return redirect(url_for(".register"))


        return redirect(url_for('main.index')) 

    # Render the user creation form for GET requests
    return render_template("auth/register.html", form=form)


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        remember_me = form.remember_me.data
        user = db.session.query(Customer).filter_by(username=username).first()
        
        # Check if the user exists and the password is correct
        if user and check_password_hash(user.password_hash, password):
            login_user(user, remember=remember_me)
            current_app.logger.info(f"User {username} logged in")
            flash(f'Logged in successfully as {username}', category='success')

            # check if next url is safe
            try:
                next = session['next']
                if not url_has_allowed_host_and_scheme(next, request.host_url):
                    return abort(400)

                return redirect(next or url_for('main.index'))
            except KeyError:
                current_app.logger.info('No next url in session')
                return redirect(url_for('main.index'))
        elif user and not check_password_hash(user.password_hash, password):
            current_app.logger.info('Invalid password')
            flash('Invalid password', category='danger')
            return redirect(url_for(".login"))
        elif not user:
            current_app.logger.info('Invalid username')
            flash('Invalid username', category='danger')
            return redirect(url_for(".login"))
        else:
            current_app.logger.info('Invalid username or password')
            flash('Invalid username or password', category='danger')
            return redirect(url_for(".login"))

    session['next'] = request.args.get('next')
    return render_template('auth/login.html', form=form)


@bp.route("/logout")
@login_required
def logout():
    username = current_user.username
    if logout_user():
        current_app.logger.info(f"User {username} logged out")
        flash(f'Logged out successfully as {username}', category='success')
    else:
        current_app.logger.info(f"User {username} failed to log out")
        flash(f'Could not log out as {username}', category='danger')
    return redirect(url_for("main.index"))



@bp.route("/detail")
@login_required
def details():
    user = db.get_or_404(Customer, current_user.id)
    if current_user == user:
        return render_template("auth/detail.html", user=user)
    else:
        return redirect(url_for("main.index"))


@bp.route("/delete", methods=["GET", "POST"])
@login_required
def delete():
    form = DeleteForm()
    if form.validate_on_submit():
        user = current_user
        try:
            db.session.delete(user)
            db.session.commit()
            flash(f"Deleted account {user.username}", category='success')
        except Exception as e:
            current_app.logger.debug(f"Failed to delete account {user.username}", exc_info=True)
            flash(f"failed to delete account {user.username}", category='danger')
        return redirect(url_for("main.index"))
    return render_template("auth/delete.html", form=form)


@bp.route("/change/password", methods=['GET', 'POST'])
@fresh_login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        current_password = form.current_password.data
        new_password = form.new_password.data

        if check_password_hash(current_user.password_hash, current_password):
            current_user.password_hash = generate_password_hash(new_password)
            db.session.commit()  # Commit the changes to the database
            flash("Password changed successfully", "success")
            return redirect(url_for("main.index"))
        else:
            flash("password given doesn't match current password", "danger")
            return redirect(url_for(".change_password"))
    return render_template("auth/change_password.html", form=form)


@bp.route("/change/username", methods=['GET', 'POST'])
@fresh_login_required
def change_username():
    form = ChangeUsernameForm()
    if form.validate_on_submit():
        new_username = form.new_username.data

        try:
            current_user.username = new_username
            db.session.commit()  # Commit the changes to the database
            flash("Username changed successfully", "success")
        except Exception as e:
            current_app.logger.debug("Failed to change username %s", new_username, exc_info=True)
            flash(f"Could not change username because of error: {e}", "danger")

        return redirect(url_for("main.index"))
    return render_template("auth/change_username.html", form=form)




@bp.route("/user-by-id/<int:id>")
def user_by_id(id):
    user = db.get_or_404(Customer, id)
    return render_template("show_user.html", user=user)

@bp.route("/user-by-username/<username>")
def user_by_username(username):
    user = db.one_or_404(
        db.select(Customer).filter_by(username=username),
        description=f"No user named '{username}'."
    )
    return render_template("show_user.html", user=user)

