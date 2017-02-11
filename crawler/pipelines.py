# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime

from pymongo import MongoClient

from notifiers import Notifier, PushBulletNotifier
from copy import copy


class Pipeline:
    @classmethod
    def from_crawler(cls, crawler):
        pass

    def open_spider(self, spider):
        pass

    def close_spider(self, spider):
        pass

    def process_item(self, item, spider):
        raise NotImplementedError()

    @staticmethod
    def complete_item(item, data):
        item.update(data)


class MongoPipeline(Pipeline):
    def __init__(self, host, port):
        self.host = host
        self.port = port

    @classmethod
    def from_crawler(cls, crawler):
        mongo_host = crawler.settings.get('MONGO_HOST')
        mongo_port = crawler.settings.get('MONGO_PORT')
        return cls(mongo_host, mongo_port)

    def open_spider(self, spider):
        self.client = MongoClient(host=self.host, port=self.port)
        self.collection = self.client['crawlers'][spider.name]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        raise NotImplementedError()


class SaveOnMongo(MongoPipeline):
    def process_item(self, item, spider):
        pk_name = item.PK
        pk_value = item.get(pk_name)
        saved = self.collection.find_one({pk_name: pk_value})
        if not saved:
            item_to_save = copy(dict(item))
            self.complete_item(item_to_save, {
                'notified': Notifier.STATUS_PENDING,
                'notified_at': None,
            })
            self.collection.insert(item_to_save)

        return item


class SendToPushBullet(Pipeline):
    def __init__(self, api_key):
        self.api_key = api_key

    @classmethod
    def from_crawler(cls, crawler):
        api_key = crawler.settings.get('PUSHBULLET_API_KEY')
        return cls(api_key)

    def open_spider(self, spider):
        self.notifier = PushBulletNotifier(self.api_key)

    def process_item(self, item, spider):
        is_notified = item.get('notified', Notifier.STATUS_PENDING) == Notifier.STATUS_NOTIFIED
        if not is_notified:
            self.notifier.notify(item)
            self.complete_item(item, {
                'notified': Notifier.STATUS_NOTIFIED,
                'notified_at': datetime.now()
            })

        return item


class UpdateNotified(MongoPipeline):
    def process_item(self, item, spider):
        pk_name = item.PK
        pk_value = item.get(pk_name)
        saved = self.collection.find_one({pk_name: pk_value})
        is_notified = saved.get('notified', Notifier.STATUS_PENDING) if saved else None

        if saved and is_notified:
            self.collection.update_one({
                '_id': saved.get('_id')
            }, {
                '$set': {
                    'notified': is_notified,
                }
            })

        return item
