from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import Table, create_engine, inspect, MetaData

Base = automap_base()

# Update these parameters to match your MySQL database details
server = 'bv-server-mysql.mysql.database.azure.com'  # Your Azure MySQL server name
database = 'myDb'  # Your MySQL database name
username = 'bodovision'  # Your MySQL username
password = 'veldig bra Grupp3'  # Your MySQL password

# Note: No need for specifying the driver when using mysql-connector-python
connection_string = f'mysql+mysqlconnector://{username}:{password}@{server}/{database}'

# Create the engine
engine = create_engine(connection_string, echo=False)

# Test the connection
try:
    with engine.connect() as connection:
        print("Connected successfully!")
except Exception as e:
    print("Connection failed:", e)

# Reflect the tables
Base.prepare(engine, reflect=True)

# Mapped classes are created with names by default matching that of the table name.
# Example: Assuming 'user' table exists in your database
User = Base.classes.user


db_session = Session(engine)

# Create an inspector object to explore the database
inspector = inspect(engine)

# Get the table names
table_names = inspector.get_table_names()


# Base.metadata.create_all(engine)

if __name__ == "__main__":
    # Print the table names
    print("Tables in the database:")
    for table_name in table_names:
        print(table_name)
        for column in inspector.get_columns(table_name):
            print(column["name"])
            for foreign_key in inspector.get_foreign_keys(table_name):
                print(foreign_key)
