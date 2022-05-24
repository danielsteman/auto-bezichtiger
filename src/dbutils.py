import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import Base

load_dotenv()

def _create_engine():
    conn = create_engine(os.getenv("DB_URL"), echo=True)
    return conn

def create_tables(connection=None, base=Base) -> None:
    if not connection:
        connection = _create_engine()
    base.metadata.create_all(connection)

def create_session() -> sessionmaker:
    engine = _create_engine()
    Session = sessionmaker(bind=engine)
    session = Session()
    return session
