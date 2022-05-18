from mapper import Mapper
from models import Listing

def test_map():
    test_data = [
        "Appartement Uiterwaardenstraat 340 1",
        "1079 DC Amsterdam (Scheldebuurt)",
        "€ 1.745 per maand",
        "65 m²",
        "3 kamers",
        "Gestoffeerd",
        "FRIS Vastgoed Management"
    ]
    mapper = Mapper(test_data)
    mapped_data = mapper.map()

    actual_map = {
        "title": "Appartement Uiterwaardenstraat 340 1",
        "address": "1079 DC Amsterdam (Scheldebuurt)",
        "price": "€ 1.745 per maand",
        "sq_meters": "65 m²",
        "n_rooms": "3 kamers",
        "interior": "Gestoffeerd",
        "broker": "FRIS Vastgoed Management"
    }
    actual_mapped_data = Listing(**actual_map)

    assert type(mapped_data) == type(actual_mapped_data)

    


    