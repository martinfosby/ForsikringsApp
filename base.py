from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import inspect



Base = automap_base()

# engine, suppose it has two tables 'user' and 'address' set up
# Define the connection parameters
server = 'bv-sqldb-free.database.windows.net'
database = 'bv-server-mysql.mysql.database.azure.com'
username = 'bodovision'
password = 'veldig bra Grupp3'
driver = 'ODBC+Driver+17+for+SQL+Server'

# Create the connection string
connection_string = f'mssql+pyodbc://{username}:{password}@{server}/{database}?driver={driver}'

# Create the engine
engine = create_engine(connection_string, echo=True)

# Test the connection
try:
    with engine.connect() as connection:
        print("Connected successfully!")
except Exception as e:
    print("Connection failed:", e)

# reflect the tables
Base.prepare(engine, reflect=True)

# mapped classes are now created with names by default
# matching that of the table name.
Contact = Base.classes.contact
Insurance = Base.classes.insurance
InsuranceCompany = Base.classes.insurance_company
Offer = Base.classes.offer
Settlement = Base.classes.settlement
UnitType = Base.classes.unit_type
User = Base.classes.user

session = Session(engine)

# rudimentary relationships are produced
session.commit()

# collection-based relationships are by default named
# "<classname>_collection"


# Create an inspector object
inspector = inspect(engine)

# Get the table names
table_names = inspector.get_table_names()

# Print the table names
print("Tables in the database:")
for table_name in table_names:
    print(table_name)