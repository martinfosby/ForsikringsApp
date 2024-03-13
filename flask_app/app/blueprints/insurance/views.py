from flask import jsonify, request
from flask_app.app.blueprints.insurance import bp
from flask_app.app.models import db, InsuranceCompany


@bp.route('/insurance/companies', methods=['GET'])
def get_insurance_companies():
    companies = InsuranceCompany.query.all()
    company_names = [company.name for company in companies]
    return jsonify(company_names)

@bp.route('/insurance/companies/add', methods=['POST'])
def add_insurance_company():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    new_company = InsuranceCompany(name=data['name'], other_field=data['other_field'])
    db.session.add(new_company)
    db.session.commit()

    return jsonify({'message': 'Insurance company added successfully'})