from flask import jsonify, request
from flask_login import login_required
from sqlalchemy import asc
from app.blueprints.api import bp
from app.extensions import db
from app.models import Company, Insurance, Settlement

@bp.route('/insurances', methods=['GET', 'POST', 'PUT', 'DELETE'])
def api_get_insurances():
    if request.method == 'GET':
        insurances = db.session.query(Insurance).all()
        serialized = [insurance.to_dict() for insurance in insurances]
        return serialized

    if request.method == 'POST':
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        new_insurance = Insurance(label=data['label'], unit_type_id=data['unit_type_id'], customer_id=data['customer_id'],
                                 value=data['value'], price=data['price'], due_date=data['due_date'], company_id=data['company_id'])
        db.session.add(new_insurance)
        db.session.commit()
        return jsonify(new_insurance)

    if request.method == 'PUT':
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        insurance = Insurance.query.get(data['id'])
        if not insurance:
            return jsonify({'error': 'Insurance not found'}), 404

        insurance.label = data['label']
        insurance.unit_type_id = data['unit_type_id']
        insurance.customer_id = data['customer_id']
        insurance.value = data['value']
        insurance.price = data['price']
        insurance.due_date = data['due_date']
        insurance.company_id = data['company_id']
        db.session.commit()
        return jsonify(insurance)
    
    if request.method == 'DELETE':
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        insurance = Insurance.query.get(data['id'])
        if not insurance:
            return jsonify({'error': 'Insurance not found'}), 404

@bp.route('/user/<int:user_id>/insurances')
def api_get_insurances_for_user(user_id: int):
    insurances = db.session.query(Insurance).where(Insurance.customer_id == user_id).all()
    return jsonify(insurances)


@bp.route('/user/<int:user_id>/settlements')
def api_get_settlements_for_user(user_id: int):
    settlements = db.session.query(Settlement)\
        .join(Settlement.insurance)\
        .where(Insurance.customer_id == user_id)\
        .order_by(asc(Settlement.id)).all()
    return jsonify(settlements)


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