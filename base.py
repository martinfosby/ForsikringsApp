from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
from sqlalchemy import inspect

# Update these parameters to match your MySQL database details
server = 'bv-server-mysql.mysql.database.azure.com'  # Your Azure MySQL server name
database = 'myDb'  # Your MySQL database name
username = 'bodovision'  # Your MySQL username
password = 'veldig bra Grupp3'  # Your MySQL password

# Note: No need for specifying the driver when using mysql-connector-python
connection_string = f'mysql+mysqlconnector://{username}:{password}@{server}/{database}'

# Create the engine
engine = create_engine(connection_string, echo=True)

Base = automap_base()
Base.prepare(engine, reflect=True)

# Access the table 'user'
User = Base.classes.user

if __name__ == "__main__":
    # Open a connection
    with engine.connect() as connection:
        # Query all rows from the 'user' table
        rows = connection.execute(User.__table__.select()).fetchall()
        
        # Iterate over the result and print each row
        for row in rows:
            print(row)

