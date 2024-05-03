from flask import redirect, render_template, url_for
from app.blueprints.insurances import bp
from app.extensions import db
from app.models import Company, Insurance, UnitType
from app.models.local import CompanyLocal, InsuranceLocal, UnitTypeLocal
from flask_login import current_user, login_required
from .forms import DropDownForm, MakeInsuranceForm
from datetime import date



from flask import flash, redirect, url_for

@bp.route('/make/insurance', methods=['GET', 'POST'])
def make_insurance():
    form = MakeInsuranceForm()
    if current_user.is_anonymous:
        form.company_id.choices = [(c.id, c.name) for c in CompanyLocal.query.all()]
        form.unit_type_id.choices = [(u.id, u.name) for u in UnitTypeLocal.query.all()]
    else:
        form.unit_type_id.choices = [(u.id, u.name) for u in UnitType.query.all()]
        form.company_id.choices = [(c.id, c.name) for c in Company.query.all()]
    if form.validate_on_submit():  # Checks if the form is submitted and the data is valid
        # Extract form data
        label = form.label.data
        unit_type_id = form.unit_type_id.data
        value = form.value.data
        price = form.price.data
        due_date = form.due_date.data
        company_id = form.company_id.data

        if not current_user.is_anonymous:
            customer_id = current_user.id
            new_insurance = Insurance(label=label, unit_type_id=unit_type_id, customer_id=customer_id, value=value,
                                  price=price, due_date=due_date, company_id=company_id)
        else:
            new_insurance = InsuranceLocal(
                label=label, value=value, price=price, due_date=due_date, company_id=company_id, unit_type_id=unit_type_id
                )

        db.session.add(new_insurance)
        db.session.commit()

        flash('Insurance registered successfully!', 'success')
        return redirect(url_for('main.index'))  # Redirect to a new page after form submission
    
    companies = db.session.execute(db.select(Company)).all()
    return render_template('insurances/make_insurance.html', form=form, companies=companies)

@bp.route('/insurances', methods=['GET', 'POST'])
def insurances_list():
    form = DropDownForm()
    if form.validate_on_submit():
        selected_option = form.insuranceStatus.data
        
        if selected_option == 'insured':
            # Run the query for insured
            current_date = date.today()
            insurances = db.session.query(Insurance).where(
                (Insurance.customer_id == current_user.id) &
                (
                    (Insurance.price > 0) &
                    (Insurance.due_date > current_date)
                )
            ).all()
        elif selected_option == 'uninsured':
            # Run the query for uninsured
            current_date = date.today()
            insurances = db.session.query(Insurance).where(
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
            insurances = db.session.execute(db.select(Insurance).where(Insurance.customer_id==current_user.id)).scalars().all()
            
        
        return render_template('insurances/insurances_list.html', insurances=insurances, form=form)
    else:
        if current_user.is_anonymous:
            insurances = db.session.query(InsuranceLocal).all()
        else:
            insurances = db.session.execute(db.select(Insurance).where(Insurance.customer_id==current_user.id)).scalars().all()
        return render_template('insurances/insurances_list.html', insurances=insurances, form=form)



