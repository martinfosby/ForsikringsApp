import select
from flask import jsonify, redirect, render_template, request, url_for
from app.blueprints.insurances import bp
from app.extensions import db
from app.models import Company, Insurance
from flask_login import current_user, login_required
from .forms import MakeInsuranceForm


@bp.route('/make/insurance', methods=['GET'])
@login_required
def make_insurance():
    form = MakeInsuranceForm()
    companies = db.session.execute(db.select(Company)).all()
    return render_template('insurances/make_insurance.html', form=form, companies=companies)

@bp.route('/insurances', methods=['GET'])
@login_required
def insurances_list():
    insurances = db.session.execute(db.select(Insurance).where(Insurance.customer_id==current_user.id)).scalars().all()
    print(current_user)
   
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