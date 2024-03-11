from insurance import insurance_bp
from database import db, InsuranceCompany



@insurance_bp.route('/')
def insurance():
    company = InsuranceCompany("Storebrand")
    db.session.add(company)
    db.session.commit()

    return ''
