from flask import current_app
from app.extensions import db
from app.models import Company, Contact, Insurance, Settlement, UnitType
from sqlalchemy.exc import IntegrityError

def add_data():
    try:
        companies_names = [
            "Coca Cola", 
            "Gjensidige", 
            "If", 
            "Storebrand", 
            "Svensk Brand", 
            "Vestas", 
            "Husqvarna", 
            "Skagen"
            ]
        companies = db.session.execute(db.select(Company.name)).scalars().all()
        for company in companies_names:
            if company not in companies:
                db.session.add(Company(name=company))

        unit_types_names = ["animal", "house", "cabin", "personal vehicle", "motorcycle", "travel", "pingpong", "car", "scooter", "bike", "motorhome", "boat", "other"]
        unit_types = db.session.execute(db.select(UnitType.name)).scalars().all()
        for unit_type in unit_types_names:
            if unit_type not in unit_types:
                db.session.add(UnitType(name=unit_type))

        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        current_app.logger.error(e)


