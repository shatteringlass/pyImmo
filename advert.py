import dataclasses

@dataclasses.dataclass
class HouseAdvert:
    ''' Class describing housing adverts '''
    adid: int
    title: str
    description: str
    price: int
    rooms: str
    size: int
    bathrooms: str
    level: str

    def to_tuple(self):
    	return (self.adid, self.title, self.description, self.price, self.rooms, self.size, self.bathrooms, self.level)

    