from configurator import Config
from dbutils import create_session
from models import Listing
from messenger import Messenger


class Loader:
    """
    1. Receives a Listing object
    2. Checks if Listing object already exists in the database
    3. Conditionally loads Listing object in the database
    4. Conditionally dispatches a Telegram message
    """
    def __init__(self, session=None):
        self.session = session if session else create_session()
        self.messenger = Messenger()

    def exists(self, data) -> bool:
        query_result = self.session.query(Listing).filter_by(address=data.address).first()
        return bool(query_result)

    def load(self, data: list[Listing]) -> bool:
        if not self.exists(data):
            self.session.add(data)
            return True
        self.session.commit()
        return False