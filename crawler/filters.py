import operator


class Base:
    def __init__(self, **filters):
        self.min_price = filters.get('min_price')
        self.max_price = filters.get('max_price')

        self.min_rooms = filters.get('min_rooms')

    @classmethod
    def from_yml(cls, **yml_content):
        return cls(**yml_content)

    def to_dict(self):
        raise NotImplementedError()


class Fotocasa(Base):
    def to_dict(self):
        filters = {
            'minPrice': self.min_price,
            'maxPrice': self.max_price,
            'minRooms': self.min_rooms,
        }

        return dict(filter(operator.itemgetter(1), filters.items()))
