from . import bp, admin
from flask import abort, render_template, request, redirect, session,flash,url_for
from flask_login import fresh_login_required, login_required, login_user, logout_user, current_user
from app.extensions import db
from app.models import Customer
from app.blueprints.auth.login_manager import load_user




@bp.route("/user/<int:id>/delete", methods=["GET", "POST"])
@login_required
def delete_user(id):
    if current_user.is_admin:
        user_to_be_deleted = db.get_or_404(Customer, id)
        db.session.delete(user_to_be_deleted)
        db.session.commit()
        flash(f"Successfully deleted user {user_to_be_deleted}", "info")
    else:
        flash("You need to be admin to access", "info")
    
    return redirect(url_for("main.index"))
