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

    def exists(self, row) -> bool:
        query_result = self.session.query(Listing).filter_by(address=row.address).first()
        return bool(query_result)

    def load(self, data: list[Listing]):
        # self.messenger.send_notification(
        #             msg=f'New listing found on Pararius:\nAddress: {data[0].address}\nPrice: {data[0].price}\nSquare meters: {data[0].sq_meters}'
        #         )
        for row in data:
            if not self.exists(row):
                self.session.add(row)
                self.messenger.send_notification(
                    msg=f'New listing found on Pararius:\nAddress: {row.address}\nPrice: {row.price}\nSquare meters: {row.sq_meters}'
                )
        self.session.commit()