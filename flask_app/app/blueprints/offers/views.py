from flask import current_app, redirect, render_template, request, url_for, flash
from . import bp
from app.extensions import db
from app.models import Company, Insurance, Offer
from flask_login import current_user, login_required
from .forms import DropDownForm
from res import string_resource
from .forms import DeleteOfferForm, MakeOfferForm
from sqlalchemy.exc import DataError
import random


@bp.route('/offers', defaults={'insurance_id': None}, methods=['GET', 'POST'])
@bp.route('/offers/<insurance_id>', methods=['GET', 'POST'])
@login_required
def offers_list(insurance_id):
    form: DropDownForm = DropDownForm()
    form.offerStatus.choices.extend([(insurance.id, insurance.label) for insurance in db.session.scalars(db.select(Insurance).where(Insurance.customer_id == current_user.id)).all()])

    if insurance_id:
        # Retrieve insurance records belonging to the current user
        insurance = db.get_or_404(Insurance, insurance_id)
        offers = db.session.scalars(db.select(Offer).join(Offer.insurance).where(Offer.insurance_id == insurance_id and Insurance.customer_id == current_user.id)).all()
        form.offerStatus.data = insurance_id
    else:
        # Retrieve offers only related to the user's insurance records
        insurance = None
        offers = db.session.scalars(db.select(Offer).join(Offer.insurance).where(Insurance.customer_id == current_user.id)).all()


    if form.validate_on_submit():
        if form.offerStatus.data == 'all':
            return redirect(url_for('offers.offers_list'))
        else:
            return redirect(url_for('offers.offers_list', insurance_id=form.offerStatus.data))

    return render_template('offers/offers_list.html', form=form, offers=offers, title=string_resource('offers_list_title'), insurance=insurance)



@bp.route('/make/offer/', defaults={'insurance_id': None}, methods=['GET', 'POST'])
@bp.route('/make/offer/<insurance_id>', methods=['GET', 'POST'])
@login_required
def make_offer(insurance_id):
    form: MakeOfferForm = MakeOfferForm()
    
    # Populate the dropdowns with data
    form.company_id.choices = [(company.id, company.name) for company in Company.query.all()]
    form.insurance_id.choices = [
        (insurance.id, insurance.label) for insurance in Insurance.query.filter_by(customer_id=current_user.id).all()
    ]
    form.company_id.data = str(random.choice(form.company_id.choices)[0])

    if insurance_id:
        form.insurance_id.data = insurance_id
        insurance = db.get_or_404(Insurance, insurance_id)
    else:
        try:
            form.insurance_id.data = str(random.choice(form.insurance_id.choices)[0])
        except IndexError:
            form.insurance_id.data = None
        insurance = None

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

    return render_template('offers/register_offer.html', form=form, title=string_resource('make_offer_title'), insurance=insurance)



@bp.route('/delete/offer/<int:offer_id>', methods=['GET', 'POST'])
@login_required
def delete_offer(offer_id):
    form: DeleteOfferForm = DeleteOfferForm()
    offer = db.get_or_404(Offer, offer_id)
    if request.method == 'GET':
        return render_template('offers/delete_offer.html', form=form, offer=offer)
    elif request.method == 'POST':
        db.session.delete(offer)
        db.session.commit()
        current_app.logger.info(string_resource('delete_offer_success'))
        flash(string_resource('delete_offer_success'), 'success')

        return redirect(url_for('offers.offers_list'))
    



@bp.route('/update/offer/<int:offer_id>', methods=['GET', 'POST'])
@login_required
def update_offer(offer_id):
    form: MakeOfferForm = MakeOfferForm()
    user_insurances = Insurance.query.filter_by(customer_id=current_user.id).all() #filtering registered insurances for the user
    form.insurance_id.choices = [(insurance.id, insurance.label) for insurance in user_insurances]
    form.company_id.choices = [(company.id, company.name) for company in Company.query.all()]

    offer = db.get_or_404(Offer, offer_id)
    if request.method == 'GET':
        form.insurance_id.data = str(offer.insurance_id)
        form.label.data = offer.label
        form.price.data = offer.price
        form.company_id.data = str(offer.company_id)
        return render_template('offers/register_offer.html', offer=offer, form=form, insurance=None, title=string_resource('update_offer_title'), update=True)
    elif request.method == 'POST':
        if form.validate_on_submit():
            offer.label = form.label.data
            offer.price = form.price.data
            offer.insurance_id = form.insurance_id.data
            offer.company_id = form.company_id.data

            try:
                db.session.commit()
                current_app.logger.info(string_resource('update_offer_success'))
                flash(string_resource('update_offer_success'), 'success')
            except DataError:
                db.session.rollback()
                current_app.logger.error(string_resource('dataerror'))
                flash(string_resource('dataerror'), 'danger')
            except Exception as e:
                db.session.rollback()
                current_app.logger.error(string_resource('unknown_error_with_error', error=e))
                flash(string_resource('unknown_error_with_error', error=e), 'danger')
        return redirect(url_for('offers.offers_list'))