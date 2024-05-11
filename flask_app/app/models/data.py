from app.extensions import db
from app.models import Company, Contact, Insurance, Settlement

def add_data():
    db.session.add(Company(name="Gjensidige"))
    db.session.add(Company(name="If"))
    db.session.add(Company(name="Storebrand"))

