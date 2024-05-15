from flask import current_app, redirect, render_template, request, url_for, flash
from app.blueprints.settlements import bp
from app.extensions import db
from app.models import Company, Settlement, Insurance
from flask_login import current_user, login_required
from sqlalchemy import asc, desc 
from sqlalchemy.exc import DataError
from .forms import DeleteSettlementForm, DropDownInsuranceForm, MakeSettlementForm
from res import string_resource

@bp.route('/make/settlement', defaults ={'insurance_id': None}, methods=['GET', 'POST'])
@bp.route('/make/settlement/<insurance_id>', methods=['GET', 'POST'])
@login_required
def make_settlement(insurance_id):
    form: MakeSettlementForm = MakeSettlementForm()
    companies = Company.query.all() 

    user_insurances = Insurance.query.filter_by(customer_id=current_user.id).all() #filtering registered insurances for the user

    form.insurance_label.choices = [(insurance.id, insurance.label) for insurance in user_insurances] #views the registered insurances in the form of a dropdown menu
    form.insurance_label.data = insurance_id if insurance_id else form.insurance_label.choices[0][0]
    insurance = db.get_or_404(Insurance, form.insurance_label.data) if insurance_id else None

    if form.validate_on_submit():
        new_settlement = Settlement(
            insurance_id=form.insurance_label.data,
            description=form.description.data,
            sum=form.sum.data
        )
        try:
            db.session.add(new_settlement)
            db.session.commit()
            flash(string_resource('make_settlement_success'), 'success')
            return redirect(url_for('settlements.settlement_list'))
        except DataError:
            db.session.rollback()
            current_app.logger.error(string_resource('dataerror'))
            flash(string_resource('dataerror'), 'danger')
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(string_resource('unknown_error_with_error', error=e))
            flash(string_resource('unknown_error_with_error', error=e), 'danger')


    return render_template('settlements/make_settlement.html', 
                           form=form, 
                           companies=companies, 
                           title=string_resource('make_settlement_title'), 
                           insurance=insurance)


@bp.route('/settlements', defaults={'insurance_id': None}, methods=['GET', 'POST'])
@bp.route('/settlements/<insurance_id>', methods=['GET'])
@login_required
def settlement_list(insurance_id):
    form: DropDownInsuranceForm = DropDownInsuranceForm()
    if insurance_id and insurance_id != 'all':
        form.settlementStatus.choices.extend((insurance.id, insurance.label) for insurance in db.session.scalars(
            db.select(Insurance)
            .where(Insurance.customer_id == current_user.id)
            .order_by(desc(Insurance.id == insurance_id))).all())

        form.settlementStatus.data = insurance_id

        settlements = db.session.scalars(db.select(Settlement)
                                         .join(Settlement.insurance)
                                         .where(Settlement.insurance_id == insurance_id and Insurance.customer_id == current_user.id)
                                         .order_by(asc(Settlement.id))).all()

        insurance = db.get_or_404(Insurance, insurance_id)
    else:
        form.settlementStatus.choices.extend((insurance.id, insurance.label) for insurance in db.session.scalars(
            db.select(Insurance)
            .where(Insurance.customer_id == current_user.id)).all())


        settlements = db.session.scalars(db.select(Settlement).join(Settlement.insurance)
                                         .where(Insurance.customer_id == current_user.id)
                                         .order_by(asc(Settlement.id))).all()
                                        

        insurance = None
    
    if form.validate_on_submit():
        return redirect(url_for('settlements.settlement_list', insurance_id=form.settlementStatus.data))
    
    return render_template(
        'settlements/settlements_list.html', 
        settlements=settlements, 
        title=string_resource('settlements_list_title'), 
        insurance=insurance,
        form=form
        )

@bp.route('/delete/settlement/<int:settlement_id>', methods=['GET', 'POST'])
@login_required
def delete_settlement(settlement_id):
    form: DeleteSettlementForm = DeleteSettlementForm()
    settlement = db.get_or_404(Settlement, settlement_id)
    if request.method == 'GET':
        return render_template('settlements/delete_settlement.html', form=form, settlement=settlement)
    elif request.method == 'POST':
        db.session.delete(settlement)
        db.session.commit()
        current_app.logger.info(string_resource('delete_settlement_success'))
        flash(string_resource('delete_settlement_success'), 'success')

        return redirect(url_for('settlements.settlement_list'))