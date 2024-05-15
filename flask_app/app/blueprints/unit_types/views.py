from flask import current_app, redirect, render_template, request, url_for, flash, redirect
from app.blueprints.unit_types import bp
from app.extensions import db
from app.models import UnitType
from flask_login import current_user, login_required

from res import string_resource
from .forms import MakeUnitTypeForm
from sqlalchemy.exc import DataError


@bp.route('/unit_types/', methods=['GET'])
@login_required
def unit_types_list():
    if request.method == 'GET':
        unit_types = db.session.scalars(db.select(UnitType)).all()

        title = string_resource('unit_types_list_title')
        return render_template('unit_types/unit_types_list.html', unit_types=unit_types, title=title)
    

@bp.route('/make/unit_type/', methods=['GET', 'POST'])
@login_required
def make_unit_type():
    if current_user.is_admin:
        form: MakeUnitTypeForm = MakeUnitTypeForm()
        if form.validate_on_submit():
            new_unit_type = UnitType(name=form.name.data)
            try:
                db.session.add(new_unit_type)
                db.session.commit()
                flash(string_resource('make_unit_type_success'), 'success')
                return redirect(url_for('main.index'))  # Redirect to a new page after form submission
            except DataError: # if data entered is too big
                db.session.rollback()
                current_app.logger.error(string_resource('dataerror'))
                flash(string_resource('dataerror'), 'danger')
            except Exception as e:
                db.session.rollback()
                current_app.logger.error(string_resource('unknown_error_with_error', error=e))
                flash(string_resource('unknown_error_with_error', error=e), 'danger')
        else:
            title = string_resource('make_unit_type_title')
            return render_template('unit_types/make_unit_type.html', form=form, title=title)
    else:
        flash(string_resource('not_admin'), 'danger')
        return redirect(url_for('main.index'))
