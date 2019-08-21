import dataclasses

@dataclasses.dataclass
class HouseAdvert:
    ''' Class describing housing adverts '''
    adid: int
    title: str
    description: str
    price: int
    rooms: int
    size: int
    bathrooms: int
    level: int
    