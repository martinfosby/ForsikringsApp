from app.extensions import db
from models import Company, Contact, Insurance, Settlement

# Company test data
db.session.add(Company(name="Gjensidige"))
db.session.add(Company(name="If"))
db.session.add(Company(name="Storebrand"))

# Insurance test data
db.session.add(Insurance(
        label="Husforsikring", 
        category_id=2, 
        user_id=1, 
        value=10000, 
        price=100, 
        due_date="2024-11-11",
        company_id=1
    )
)
db.session.add(Insurance(
        label="Bilforsikring", 
        category_id=4, 
        user_id=1, 
        value=5000, 
        price=100, 
        due_date="2024-11-11",
        company_id=1
    )
)

db.session.add()