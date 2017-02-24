from lib import config
from lib import mongo


def make_mongo_client():
    host = config.MONGO_HOST
    port = config.MONGO_PORT
    database = config.MONGO_DATABASE
    return mongo.Client(host, port, database)
