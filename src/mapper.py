from models import Listing


class Mapper:
    def __init__(self, data: list[str]):
        self.data = data
        self.mapped_data = None

    def _move_item_to_end(self, index: int):
        self.data.append(self.data.pop(index))

    def _get_fields(self, table):
        return [
            field.name
            for field in
            table.__table__.columns
            if not field.primary_key
        ]

    def _map_values(self, table):
        fields = self._get_fields(table)
        return {
            field: value 
            for field, value in
            dict(zip(fields, self.data)).items()
        }

    def map(self):
        values = self._map_values(Listing)
        self.mapped_data = Listing(**values)

    def __repr__(self):
        return "{}({!r})".format(self.__class__.__name__, self.__dict__)