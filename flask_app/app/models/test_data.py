from os import name
from app.extensions import db
from . import Company, Contact, Insurance, Settlement
from .local import InsuranceLocal, CompanyLocal, UnitTypeLocal

# Company test data

def add_local_test_data():
    db.session.add(CompanyLocal(name="Gjensidige"))
    db.session.add(CompanyLocal(name="If"))
    db.session.add(CompanyLocal(name="Storebrand"))
    db.session.add(CompanyLocal(name="Tryg"))

    db.session.add(UnitTypeLocal(name="Hus"))
    db.session.add(UnitTypeLocal(name="Bil"))
    db.session.add(UnitTypeLocal(name="Familiebarn"))


    db.session.commit()

# db.session.add(Company(name="Gjensidige"))
# db.session.add(Company(name="If"))
# db.session.add(Company(name="Storebrand"))

# Insurance test data
# db.session.add(Insurance(
#         label="Husforsikring", 
#         category_id=2, 
#         user_id=1, 
#         value=10000, 
#         price=100, 
#         due_date="2024-11-11",
#         company_id=1
#     )
# )
# db.session.add(Insurance(
#         label="Bilforsikring", 
#         category_id=4, 
#         user_id=1, 
#         value=5000, 
#         price=100, 
#         due_date="2024-11-11",
#         company_id=1
#     )
# )
