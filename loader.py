import logging
from dbutils import create_session
from models import Listing


class Loader:
    def __init__(self, session=None):
        self.session = session if session else create_session()

    def exists(self, data):
        addresses = [l.address for l in data]
        result = self.session.query(Listing).filter(Listing.address.in_(addresses))
        return result

    def load(self, data):
        print(self.exists(data))
        # if self.exists(data):
        #     logging.info(f"{data} is already registered")
        # else:
        #     self.session.add_all(data)
        #     logging.info(f"registered: {data}")
        # self.session.commit()