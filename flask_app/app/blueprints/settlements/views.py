from flask import current_app, redirect, render_template, url_for
from app.blueprints.settlements import bp
from app.extensions import db
from app.models import Company, Settlement, Insurance
from flask_login import current_user, login_required
from sqlalchemy import asc 
from sqlalchemy.exc import DataError
from .forms import MakeSettlementForm

from flask import flash, redirect, url_for
from res import string_resource

@bp.route('/make/settlement', methods=['GET', 'POST'])
@login_required
def make_settlement():
    form = MakeSettlementForm()
    companies = Company.query.all() 

    user_insurances = Insurance.query.filter_by(customer_id=current_user.id).all() #filtering registered insurances for the user

    form.insurance_label.choices = [(insurance.id, insurance.label) for insurance in user_insurances] #views the registered insurances in the form of a dropdown menu

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
            return redirect(url_for('main.index'))
        except DataError:
            db.session.rollback()
            current_app.logger.error(string_resource('dataerror'))
            flash(string_resource('dataerror'), 'danger')
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(string_resource('unknown_error_with_error', error=e))
            flash(string_resource('unknown_error_with_error', error=e), 'danger')


    return render_template('settlements/make_settlement.html', form=form, companies=companies, title=string_resource('make_settlement_title'))



@bp.route('/settlements', methods=['GET'])
@login_required
def settlement_list():
    settlements = db.session.query(Settlement)\
        .join(Settlement.insurance)\
        .where(Insurance.customer_id == current_user.id)\
        .order_by(asc(Settlement.id)).all()
    

    return render_template('settlements/settlements_list.html', settlements=settlements, title=string_resource('settlements_list_title'))