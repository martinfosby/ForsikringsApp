from flask import redirect, render_template, url_for
from app.blueprints.settlements import bp
from app.extensions import db
from app.models import Company, Settlement, Insurance
from flask_login import current_user, login_required
from sqlalchemy import asc 
from .forms import MakeSettlementForm

from flask import flash, redirect, url_for


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
        db.session.add(new_settlement)
        db.session.commit()
        flash('Settlement registered successfully!', 'success')
        return redirect(url_for('main.index'))


    return render_template('settlements/make_settlement.html', form=form, companies=companies)



@bp.route('/settlements', methods=['GET'])
@login_required
def settlement_list():
    settlements = db.session.query(Settlement)\
        .join(Settlement.insurance)\
        .where(Insurance.customer_id == current_user.id)\
        .order_by(asc(Settlement.id)).all()
    

    return render_template('settlements/settlements_list.html', settlements=settlements)