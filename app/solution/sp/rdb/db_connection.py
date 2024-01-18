from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.exc import OperationalError
from typing import Annotated
from config import DB_NAME,DB_USERNAME,DB_PASSWORD,DB_HOST
import time



DATABASE_URI = f'postgresql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:5432/{DB_NAME}'

    
def is_database_ready(database_url, max_retries=10, retry_interval=5):
    retries = 0
    while retries < max_retries:
        try:
            test_engine = create_engine(database_url)
            with test_engine.connect() as connection:
                connection.execute(text("SELECT 1"))
            return True  
        except OperationalError:
            time.sleep(retry_interval)
            retries += 1
    return False

if is_database_ready(DATABASE_URI):
    print("Database is ready. Starting the application.")
else:
    print("Database is not ready. Exiting.")

engine = create_engine(DATABASE_URI)
try:
    if not database_exists(engine.url):
        create_database(engine.url)
        print(f"Database '{DB_NAME}' created successfully!")
    engine = create_engine(DATABASE_URI)

except OperationalError as e:
    print("An error occurred:", e)
    
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

    
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
