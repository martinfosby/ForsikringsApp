from flask import current_app, jsonify, redirect, render_template, request, url_for
from app.blueprints.insurances import bp
from app.extensions import db
from app.models import Company, Insurance, UnitType
from flask_login import current_user, login_required
from .forms import MakeInsuranceForm


from flask import flash, redirect, url_for

@bp.route('/make/insurance', methods=['GET', 'POST'])
@login_required
def make_insurance():
    form = MakeInsuranceForm()
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
        db.session.add(new_insurance)
        db.session.commit()

        flash('Insurance registered successfully!', 'success')
        return redirect(url_for('main.index'))  # Redirect to a new page after form submission
    
    companies = db.session.execute(db.select(Company)).all()
    return render_template('insurances/make_insurance.html', form=form, companies=companies)

@bp.route('/insurances', methods=['GET'])
@login_required
def insurances_list():
    insurances = db.session.execute(db.select(Insurance).where(Insurance.customer_id==current_user.id)).scalars().all()
    current_app.logger.info(current_user)
   
    return render_template('insurances/insurances_list.html', insurances=insurances, user=current_user)

@bp.route('/companies', methods=['GET'])
@login_required
def get_insurance_companies():
    companies = Company.query.all()
    company_names = [company.name for company in companies]
    return jsonify(company_names)


@bp.route('/company/add', methods=['POST'])
@login_required
def add_insurance_company():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    new_company = Company(name=data['name'], other_field=data['other_field'])
    db.session.add(new_company)
    db.session.commit()

    return jsonify({'message': 'Insurance company added successfully'})