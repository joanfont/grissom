from pymongo import MongoClient


class Client:
    def __init__(self, host, port, database):
        self.host = host
        self.port = port
        self.database = database

        self.mongo = None

    def close(self):
        if self.mongo:
            self.mongo.close()

    def _init_mongo(self):
        if not self.mongo:
            self.mongo = MongoClient(host=self.host, port=self.port)

    def _get_database(self):
        return self.mongo[self.database]

    def _get_collection(self, collection):
        return self._get_database()[collection]

    def __enter__(self):
        self._init_mongo()
        return self._get_database()

    def __exit__(self, *args):
        self.close()

    def __getitem__(self, item):
        self._init_mongo()
        return self.mongo[self.database][item]
