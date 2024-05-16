from flask import current_app
from app.extensions import db
from app.models import Company, Contact, Insurance, Offer, Settlement, UnitType
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



def add_test_data():
    try:
        from datetime import datetime, timedelta
        # Get today's date
        today = datetime.now().date()

        insurances = [
            { 
                "label": "min husforsikring i bloksberg", 
                "company_id": 1, 
                "unit_type_id": 2, 
                "customer_id": 55, 
                "price": 100, 
                "value": 50000,
                "due_date": today + timedelta(days=30)
            },
            { 
                "label": "min husforsikring i vestborgsund", 
                "company_id": 2, 
                "unit_type_id": 2, 
                "customer_id": 55, 
                "price": 120, 
                "value": 70000,
                "due_date": today + timedelta(days=60)
            },
            { 
                "label": "min husforsikring i gaza", 
                "company_id": 3, 
                "unit_type_id": 3, 
                "customer_id": 55, 
                "price": 150, 
                "value": 80000,
                "due_date": today + timedelta(days=90)
            },
            { 
                "label": "kristiansands eiendomforsikring", 
                "company_id": 3, 
                "unit_type_id": 2, 
                "customer_id": 55, 
                "price": 80, 
                "value": 60000,
                "due_date": today + timedelta(days=120)
            },
            { 
                "label": "rudolf larsens båtforsikring", 
                "company_id": 3, 
                "unit_type_id": 8, 
                "customer_id": 55, 
                "price": 200, 
                "value": 30000,
                "due_date": today + timedelta(days=150)
            },
            { 
                "label": "universitetets studentforsikring", 
                "company_id": 3, 
                "unit_type_id": 58, 
                "customer_id": 55, 
                "price": 180, 
                "value": 40000,
                "due_date": today + timedelta(days=180)
            },
            { 
                "label": "usa reise forsikring", 
                "company_id": 1, 
                "unit_type_id": 10, 
                "customer_id": 55, 
                "price": 210, 
                "value": 90000,
                "due_date": today + timedelta(days=210)
            },
            { 
                "label": "pcforsikring", 
                "company_id": 2, 
                "unit_type_id": 58, 
                "customer_id": 55, 
                "price": 250, 
                "value": 55000,
                "due_date": today + timedelta(days=240)
            },
            { 
                "label": "scooterforsikring", 
                "company_id": 1, 
                "unit_type_id": 55, 
                "customer_id": 55, 
                "price": 300, 
                "value": 15000,
                "due_date": today + timedelta(days=270)
            },
            { 
                "label": "stolforsikring", 
                "company_id": 2, 
                "unit_type_id": 58, 
                "customer_id": 55, 
                "price": 180, 
                "value": 45000,
                "due_date": today + timedelta(days=300)
            },
            { 
                "label": "veggforsikring", 
                "company_id": 1, 
                "unit_type_id": 58, 
                "customer_id": 55, 
                "price": 200, 
                "value": 35000,
                "due_date": today + timedelta(days=330)
            },
            { 
                "label": "stolpeforsikring", 
                "company_id": 1, 
                "unit_type_id": 58, 
                "customer_id": 55, 
                "price": 250, 
                "value": 50000,
                "due_date": today + timedelta(days=360)
            },
            { 
                "label": "bussforsikring", 
                "company_id": 2, 
                "unit_type_id": 60, 
                "customer_id": 55, 
                "price": 280, 
                "value": 60000,
                "due_date": today + timedelta(days=390)
            },
            { 
                "label": "gulvforsikring", 
                "company_id": 3, 
                "unit_type_id": 58, 
                "customer_id": 55, 
                "price": 230, 
                "value": 48000,
                "due_date": today + timedelta(days=420)
            },
            # Add more dictionaries as needed
        ]

        settlements = [
            { "insurance_id": 82, "description": "tyver gikk inn og stjall varene", "sum": 10000},
            { "insurance_id": 83, "description": "tyver gikk inn og stjall vegene", "sum": 10000},
            { "insurance_id": 84, "description": "taket raste", "sum": 100000},
            { "insurance_id": 85, "description": "veget ble tatt av storm", "sum": 56000},
            { "insurance_id": 86, "description": "båten mistet motoren", "sum": 56000},
            { "insurance_id": 87, "description": "studenter stjal bøkene mine", "sum": 56000},
        ]

        offers = [
            { "label" : "tilbud på husforsikring 5000kr", "price": 5000, "insurance_id": 82, "company_id": 1},
            { "label" : "tilbud på båtforsikring 10000kr", "price": 10000, "insurance_id": 86, "company_id": 1},
            { "label" : "tilbud på stolpeforsikring", "price": 20000, "insurance_id": 91, "company_id": 1},
            { "label" : "tilbud på gulvforsikring 220000kr", "price": 220000, "insurance_id": 95, "company_id": 1},
        ]

        insurances_from_db = db.session.scalars(db.select(Insurance)).all()
        settlements_from_db = db.session.scalars(db.select(Settlement)).all()
        offers_from_db = db.session.scalars(db.select(Offer)).all()
        # for insurance in insurances:
        #     insur = Insurance(**insurance)
        #     if insur not in insurances_from_db:
        #         db.session.add(insur)
        # db.session.commit()


        for settlement in settlements:
            setl = Settlement(**settlement)
            if setl not in settlements_from_db:
                db.session.add(setl)
        db.session.commit()

        for offer in offers:
            offe = Offer(**offer)
            if offe not in offers_from_db:
                db.session.add(offe)

        db.session.commit()
    except IntegrityError as e:
        db.session.rollback()
        current_app.logger.error(e)

