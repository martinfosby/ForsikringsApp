import select
from flask import jsonify, redirect, render_template, request, url_for
from flask_app.app.blueprints.insurance import bp
from flask_app.app.extensions import db
from flask_app.app.models import InsuranceCompany, Insurance


@bp.route('/insurances', methods=['GET'])
def insurance_list():
    insurances = db.session.execute(db.select(Insurance)).scalars().all()
    html_response = "<h1>Insurances:</h1>"
    
    # Using lambda directly within the loop to format each insurance object
    for insurance in insurances:
        html_response += f"<p>{insurance.label}</p><br>"
    
    return html_response

@bp.route('/companies', methods=['GET'])
def get_insurance_companies():
    companies = InsuranceCompany.query.all()
    company_names = [company.name for company in companies]
    return jsonify(company_names)

@bp.route('/company/add', methods=['POST'])
def add_insurance_company():
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    new_company = InsuranceCompany(name=data['name'], other_field=data['other_field'])
    db.session.add(new_company)
    db.session.commit()

    return jsonify({'message': 'Insurance company added successfully'})