from dataclasses import dataclass


@dataclass
class Listing:
    platform: str
    title: str
    address: str
    price: str
    sq_meters: str
    n_rooms: str
    interior: str
    broker: str
    status: str = "Geen status"