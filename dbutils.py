import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base

load_dotenv()

def create_connection():
    conn = create_engine(os.getenv("DB_URL"), echo=True)
    return conn

def create_tables(connection=None, base=Base):
    if not connection:
        connection = create_connection()
    base.metadata.create_all(connection)

def create_session():
    engine = create_connection()
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
