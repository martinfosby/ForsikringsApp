import select
from flask import jsonify, redirect, render_template, request, url_for
from flask_app.app.blueprints.insurances import bp
from flask_app.app.extensions import db
from flask_app.app.models import Company, Insurance


@bp.route('/make/insurance', methods=['GET'])
def make_insurance():
    return render_template('insurances/make_insurance.html')

@bp.route('/insurances', methods=['GET'])
def insurances_list():
    insurances = db.session.execute(db.select(Insurance)).scalars().all()
   
    return render_template('insurances/insurances_list.html', insurances=insurances)

@bp.route('/companies', methods=['GET'])
def get_insurance_companies():
    companies = Company.query.all()
    company_names = [company.name for company in companies]
    return jsonify(company_names)

@bp.route('/company/add', methods=['POST'])
def add_insurance_company():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    new_company = Company(name=data['name'], other_field=data['other_field'])
    db.session.add(new_company)
    db.session.commit()

    return jsonify({'message': 'Insurance company added successfully'})