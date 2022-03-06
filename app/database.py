from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from psycopg2.extras import RealDictCursor  ##To rerturn the column name with the query (by default it is not available)
from .config import settings


SQL_ALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'

## Creating Engine- This is reponsible for SQl Alchemy to connect to postgres database

engine = create_engine(SQL_ALCHEMY_DATABASE_URL)


##To talk to SQL database, create a session

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


## All the class that be created will extend this base class
Base = declarative_base()

# Dependency
#Creates connection with the database and then close the connection once the
#Operation has been performed

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', dbname='fastapi', user='postgres', password=1234, cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection was successful')
#         break

#     except Exception as error:
#         print('connection to database failed')
#         print("Error: ",error)
#         time.sleep(2)