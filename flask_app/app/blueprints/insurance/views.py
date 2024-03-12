from flask_app.app.blueprints.insurance import bp
from flask_app.app.models import db, InsuranceCompany



@bp.route('/')
def insurance():
    company = InsuranceCompany("Storebrand")
    db.session.add(company)
    db.session.commit()

    return ''
