from urllib.parse import urlencode

from lib import number_to_text


class Base:
    SITE = None

    def build(self, **filters):
        raise NotImplementedError()

    @staticmethod
    def clean_empty(data):
        return {k: v for k, v in data.items() if v is not None}


class Fotocasa(Base):
    SITE = 'fotocasa'

    def build(self, **filters):
        filters = self.clean_empty({
            'minPrice': filters.get('min_price'),
            'maxPrice': filters.get('max_price'),
            'minRooms': filters.get('min_rooms'),
        })

        return urlencode(filters)


class Idealista(Base):
    SITE = 'idealista'

    MAX_ROOMS = 4

    def build(self, **filters):
        filter_parts = []

        if filters.get('min_price'):
            min_price = filters.get('min_price')
            min_price_filter = f'precio-desde_{min_price}'
            filter_parts.append(min_price_filter)

        if filters.get('max_price'):
            max_price = filters.get('max_price')
            max_price_filter = f'precio-hasta_{max_price}'
            filter_parts.append(max_price_filter)

        if filters.get('min_rooms', 0) >= 0:  # as 0 is a valid value for the filter
            min_rooms = filters.get('min_rooms')
            min_rooms_filter = self._build_min_rooms(min_rooms)
            filter_parts.extend(min_rooms_filter)

        if not filter_parts:
            return None

        filter_string = ','.join(filter_parts)
        return f'con-{filter_string}'

    @classmethod
    def _build_min_rooms(cls, min_rooms):
        if not min_rooms:
            return ['estudios']

        return list(
            map(cls._get_room_filter, range(min_rooms, cls.MAX_ROOMS + 1))
        )

    @classmethod
    def _get_room_filter(cls, number):
        if number == 1:
            number_word = number_to_text(number)
            suffix = 'dormitorio'
        elif number >= 4:
            four_str = number_to_text(4)
            five_str = number_to_text(5)
            number_word = f'{four_str}-{five_str}'
            suffix = 'habitaciones-o-mas'
        else:
            number_word = number_to_text(number)
            suffix = 'dormitorios'

        return f'de-{number_word}-{suffix}'


class Factory:
    SITES = {
        Fotocasa.SITE: Fotocasa,
        Idealista.SITE: Idealista,
    }

    @classmethod
    def build(cls, site):
        filter_class = cls.SITES.get(site)
        if not filter_class:
            return None

        return filter_class()
