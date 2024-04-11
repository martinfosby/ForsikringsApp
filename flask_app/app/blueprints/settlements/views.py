import select
from flask import jsonify, redirect, render_template, request, url_for
from app.blueprints.settlements import bp
from app.extensions import db
from app.models import Company, Settlement
from flask_login import current_user, login_required
from .forms import MakeSettlementForm

from flask import flash, redirect, url_for


@bp.route('/make/settlement', methods=['GET', 'POST'])
@login_required
def make_settlement():
    form = MakeSettlementForm()
    companies = Company.query.all() 
    if form.validate_on_submit():

        new_settlement = Settlement(
            insurance_id=form.insurance_id.data,
            description=form.description.data,
            sum=form.sum.data
        )
        db.session.add(new_settlement)
        db.session.commit()
        flash('Settlement registered successfully!', 'success')
        return redirect(url_for('main.index')) 

    return render_template('settlements/make_settlement.html', form=form, companies=companies)