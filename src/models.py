from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class Listing(Base):
    __tablename__ = "listings"

    id = Column(Integer, primary_key=True)
    title = Column(String, unique=True)
    address = Column(String, unique=True)
    price = Column(String)
    sq_meters = Column(String)
    n_rooms = Column(String)
    interior = Column(String)
    broker = Column(String)
    status = Column(String, default="Geen status")
    website = Column(String, default="Pararius")

    def __repr__(self) -> str:
        return "{}({!r})".format(self.__class__.__name__, self.__dict__)