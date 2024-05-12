from flask import current_app, redirect, render_template, url_for, flash
from app.blueprints.offers import bp
from app.extensions import db
from app.models import Company, Insurance, Offer
from flask_login import current_user, login_required

from res import string_resource
from .forms import MakeOfferForm
from sqlalchemy.exc import DataError


@bp.route('/offers', methods=['GET', 'POST'])
def offers_list():
    # Retrieve insurance records belonging to the current user
    user_insurances = Insurance.query.filter_by(customer_id=current_user.id).all()
    insurance_ids = [insurance.id for insurance in user_insurances]

    # Retrieve offers only related to the user's insurance records
    offers = Offer.query.filter(Offer.insurance_id.in_(insurance_ids)).all()

    return render_template('offers/offers_list.html', offers=offers, title=string_resource('offers_list_title'))



@bp.route('/make/offer/', methods=['GET', 'POST'])
@login_required
def make_offer():
    form = MakeOfferForm()
    
    # Populate the dropdowns with data
    form.company_id.choices = [(company.id, company.name) for company in Company.query.all()]
    form.insurance_id.choices = [
        (insurance.id, insurance.label) for insurance in Insurance.query.filter_by(customer_id=current_user.id).all()
    ]

    if form.validate_on_submit():
        # Process the form data and save the offer
        offer = Offer(
            label=form.label.data,
            price=form.price.data,
            company_id=form.company_id.data,
            insurance_id=form.insurance_id.data
        )
        try:
            db.session.add(offer)
            db.session.commit()
            flash(string_resource("make_offer_success"), 'success')
            return redirect(url_for('offers.offers_list'))
        except DataError: # if data entered is too big
            db.session.rollback()
            current_app.logger.error(string_resource('dataerror'))
            flash(string_resource('dataerror'), 'danger')
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(string_resource('unknown_error_with_error', error=e))
            flash(string_resource('unknown_error_with_error', error=e), 'danger')

    return render_template('offers/register_offer.html', form=form, title=string_resource('make_offer_title'))