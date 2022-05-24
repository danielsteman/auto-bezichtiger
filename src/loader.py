import logging
from dbutils import create_session
from models import Listing


class Loader:
    """
    1. Receives a Listing object
    2. Checks if Listing object already exists in the database
    3. Conditionally loads Listing object in the database
    4. Conditionally dispatches a Telegram message
    """
    def __init__(self, session=None):
        self.session = session

    def _exists(self, data: Listing) -> bool:
        query_result = self.session.query(Listing).filter_by(address=data.address).first()
        return bool(query_result)

    def load(self, data: Listing) -> bool:
        new_listing = False
        if not self.session:
            self.session = create_session()
        if not self._exists(data):
            self.session.add(data)
            self.session.commit()
            logging.info(f"New listing found: {data}")
            new_listing = True
        self.session.close()
        return new_listing