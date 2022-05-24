class Transformer:
    def __init__(self, data, mapper, estate_agent):
        self.data = data
        self.mapper = mapper
        self.estate_agent = estate_agent

    def group_items(lst: list, size: int):
        return list(zip(*(iter(lst),) * size))

    def transform(self):

        match self.estate_agent:

            case 'pararius':
                parsed_data = [listing.split('\n') for listing in self.data]
                mapped_data = []

                for row in parsed_data:
                    mapper = self.mapper(row)
                    if len(row) == 8:
                        mapper._move_item_to_end(0)
                    mapper.map()
                    mapped_data.append(mapper.mapped_data)
                return mapped_data

            case 'vesteda':
                exclude_values = ["slaap\xadkamer(s)", "Appartement", "per maand", "Oppervlakte", "BEKIJK WONING"]
                data = [i.split('\n') for i in self.data]
                filtered_data = [word for sentence in data for word in sentence if word not in exclude_values]
                parsed_data = self.group_items(filtered_data, 6)
                mapped_data = []

                for row in parsed_data:
                    transformed_row = ['Appartement', row[3], row[5], row[1], row[0], 'Interieur onbekend', 'Makelaar onbekend', row[2], self.estate_agent]
                    mapper = self.mapper(transformed_row)
                    mapper.map()
                    mapped_data.append(mapper.mapped_data)
                return mapped_data