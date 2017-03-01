from urllib.parse import urlparse

from lib import config
from lib import mongo

NUMBER_MAPPING = {
    0: 'cero',
    1: 'un',
    2: 'dos',
    3: 'tres',
    4: 'cuatro',
    5: 'cinco',
    6: 'seis',
    7: 'siete',
    8: 'ocho',
    9: 'nueve',
}

MAX_NUMBER = 9


def make_mongo_client():
    host = config.MONGO_HOST
    port = config.MONGO_PORT
    database = config.MONGO_DATABASE
    return mongo.Client(host, port, database)


def remove_querystring_from_url(url):
    parsed_url = urlparse(url)
    if not parsed_url:
        return url

    return f'{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}'


def number_to_text(number):
    if number > MAX_NUMBER:
        raise ValueError()

    return NUMBER_MAPPING.get(number)
