from flask import current_app, redirect, render_template, request, url_for, flash, redirect
from app.blueprints.companies import bp
from app.extensions import db
from app.models import Company
from flask_login import current_user, login_required

from res import string_resource
from .forms import MakeCompanyForm
from sqlalchemy.exc import DataError





@bp.route('/companies', methods=['GET'])
@login_required
def companies_list():
    if request.method == 'GET':
        companies = db.session.scalars(db.select(Company)).all()
        return render_template('companies/companies_list.html', companies=companies, title=string_resource('companies_list_title'))
    

@bp.route('/make/company', methods=['GET', 'POST'])
@login_required
def make_company():
    if current_user.is_admin:
        form: MakeCompanyForm = MakeCompanyForm()
        if form.validate_on_submit():
            new_company = Company(name=form.name.data)
            try:
                db.session.add(new_company)
                db.session.commit()
                flash(string_resource('make_company_success'), 'success')
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
            return render_template('companies/make_company.html', form=form)
    else:
        flash(string_resource('not_admin'), 'danger')
        return redirect(url_for('main.index'))
