from os import name
from app.extensions import db
from . import Company, Contact, Insurance, Settlement

# Company test data

def add_company_data():
    db.session.add(Company(name="Gjensidige"))
    db.session.add(Company(name="If"))
    db.session.add(Company(name="Storebrand"))

