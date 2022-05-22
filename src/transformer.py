class Transformer:
    def __init__(self):
        return self

    def _extract_digits(self, s: str):
        return int(''.join([i for i in s if i.isdigit()]))


class ParariusTransformer(Transformer):
    def __init__(self, data, mapper):
        self.data = data
        self.mapper = mapper

    def transform(self):
        parsed_data = [listing.split('\n') for listing in self.data]
        mapped_data = []

        for line in parsed_data:
            mapper = self.mapper(line)
            if len(line) == 8:
                mapper._move_item_to_end(0)
            mapper.map()
            mapped_data.append(mapper.mapped_data)
        return mapped_data

    