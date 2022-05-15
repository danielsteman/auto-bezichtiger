import logging
from dbutils import create_session
from models import Listing


class Loader:
    def __init__(self, session=None):
        self.session = session if session else create_session()

    def exists(self, row):
        query_result = self.session.query(Listing).filter_by(address=row.address).first()
        return bool(query_result)

    def load(self, data):
        for row in data:
            if not self.exists(row):
                self.session.add(row)
        self.session.commit()