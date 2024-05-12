from turtle import title
from flask import current_app, redirect, render_template, request, url_for, flash, redirect
from app.blueprints.contacts import bp
from app.extensions import db
from app.models import Company, Contact
from flask_login import current_user, login_required

from res import string_resource
from .forms import MakeContactForm
from sqlalchemy.exc import DataError




@bp.route('/contacts/', defaults={'company_id': None}, methods=['GET'])
@bp.route('/contacts/<company_id>', methods=['GET'])
@login_required
def contacts_list(company_id):
    if request.method == 'GET':
        if company_id:
            contacts = db.session.scalars(db.select(Contact).where(Contact.company_id == company_id)).all()
        else:
            contacts = db.session.scalars(db.select(Contact)).all()

        title = string_resource('contacts_list_title')
        return render_template('contacts/contacts_list.html', contacts=contacts, title=title)
    

@bp.route('/make/contact', methods=['GET', 'POST'])
@login_required
def make_contact():
    if current_user.is_admin:
        form: MakeContactForm = MakeContactForm()
        form.company.choices=[(c.id, c.name) for c in db.session.scalars(db.select(Company)).all()]
        if form.validate_on_submit():
            new_contact = Contact(company_id=form.company.data, name=form.name.data, phone_number=form.phone_number.data, email=form.email.data)
            try:
                db.session.add(new_contact)
                db.session.commit()
                flash(string_resource('make_contact_success'), 'success')
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
            title = string_resource('make_contact_title')
            return render_template('contacts/make_contact.html', form=form, title=title)
    else:
        flash(string_resource('not_admin'), 'danger')
        return redirect(url_for('main.index'))
