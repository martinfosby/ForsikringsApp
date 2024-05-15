from flask import current_app, redirect, render_template, url_for, flash, redirect
from app.blueprints.insurances import bp
from app.extensions import db
from app.models import Company, Insurance, UnitType
from flask_login import current_user, login_required

from res import string_resource
from .forms import DropDownForm, MakeInsuranceForm
from datetime import date
from sqlalchemy.exc import DataError


@bp.route('/make/insurance', methods=['GET', 'POST'])
@login_required
def make_insurance():
    form: MakeInsuranceForm = MakeInsuranceForm()
    form.unit_type_id.choices = [(u.id, u.name) for u in UnitType.query.all()]
    form.company_id.choices = [(c.id, c.name) for c in Company.query.all()]
    if form.validate_on_submit():  # Checks if the form is submitted and the data is valid
        # Extract form data
        customer_id = current_user.id
        label = form.label.data
        unit_type_id = form.unit_type_id.data
        value = form.value.data
        price = form.price.data
        due_date = form.due_date.data
        company_id = form.company_id.data

        # Here, you can create a new Insurance object and save it to the database
        # Assuming you have an Insurance model with appropriate fields
        new_insurance = Insurance(label=label, unit_type_id=unit_type_id, customer_id=customer_id, value=value,
                                  price=price, due_date=due_date, company_id=company_id)
        try:
            db.session.add(new_insurance)
            db.session.commit()
            current_app.logger.info(string_resource('make_insurance_success'))
            flash(string_resource('make_insurance_success'), 'success')
            return redirect(url_for('main.index'))  # Redirect to a new page after form submission
        except DataError: # if data entered is too big
            db.session.rollback()
            current_app.logger.error(string_resource('dataerror'))
            flash(string_resource('dataerror'), 'danger')
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(string_resource('unknown_error_with_error', error=e))
            flash(string_resource('unknown_error_with_error', error=e), 'danger')
    elif form.errors:
        # Handle validation errors
        current_app.logger.error(form.errors)
        for field, errors in form.errors.items():
            for error in errors:
                if field == 'due_date':
                    flash(f'{"Due date"}: {error}', 'danger')
                else:
                    flash(f'{field}: {error}', 'danger')
    
    companies = db.session.execute(db.select(Company)).all()
    return render_template('insurances/make_insurance.html', form=form, companies=companies, title=string_resource('make_insurance_title'))

@bp.route('/insurances', methods=['GET', 'POST'])
@login_required
def insurances_list():
    title=string_resource('insurances_list_title')
    form = DropDownForm()
    if form.validate_on_submit():
            selected_option = form.insuranceStatus.data
            
            if selected_option == 'insured':
                # Run the query for insured
                current_date = date.today()
                insurances = db.session.query(Insurance).join(Insurance.unit_type).where(
                    (Insurance.customer_id == current_user.id) &
                    (
                        (Insurance.price > 0) &
                        (Insurance.due_date > current_date)
                    )
                ).all()
            elif selected_option == 'uninsured':
                # Run the query for uninsured
                current_date = date.today()
                insurances = db.session.query(Insurance).join(Insurance.unit_type).where(
                    (Insurance.customer_id == current_user.id) &
                    (
                        (Insurance.price == 0) | 
                        (Insurance.price == None) |
                        (Insurance.due_date <= current_date) | 
                        (Insurance.due_date == None)
                    )
                ).all()
            else:
                # Handle other cases or set a default query
                insurances = db.session.scalars(db.select(Insurance).join(Insurance.unit_type)
                                                .where(Insurance.customer_id==current_user.id)).all()
            
            return render_template('insurances/insurances_list.html', insurances=insurances, form=form, title=title)
    else:
        insurances = db.session.scalars(db.select(Insurance).join(Insurance.unit_type).where(Insurance.customer_id==current_user.id)).all()
        return render_template('insurances/insurances_list.html', insurances=insurances, form=form, title=title)



