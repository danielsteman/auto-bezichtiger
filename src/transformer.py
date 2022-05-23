class Transformer:
    def __init__(self, data, mapper, estate_agent):
        self.data = data
        self.mapper = mapper
        self.estate_agent = estate_agent

    def transform(self):

        match self.estate_agent:

            case 'pararius':
                parsed_data = [listing.split('\n') for listing in self.data]
                mapped_data = []

                for line in parsed_data:
                    mapper = self.mapper(line)
                    if len(line) == 8:
                        mapper._move_item_to_end(0)
                    mapper.map()
                    mapped_data.append(mapper.mapped_data)
                return mapped_data

            case 'vesteda':
                exclude_values = ["slaap\\xadkamer(s)"]
                parsed_data = [i.split('\n') for i in self.data]
                data = [word for sentence in parsed_data for word in sentence if word not in exclude_values]
                