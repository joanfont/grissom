# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Item(scrapy.Item):
    CRAWLER_NAME = None
    SITE_NAME = None
    PK = None

    title = scrapy.Field()
    url = scrapy.Field()
    description = scrapy.Field()
    price = scrapy.Field()

    town = scrapy.Field()

    rooms = scrapy.Field()
    bathrooms = scrapy.Field()
    area = scrapy.Field()

    def to_dict(self):
        item_dict = dict(self)
        item_dict.update({
            'crawler': self.CRAWLER_NAME,
            'site': self.SITE_NAME,
            'pk': self.PK
        })

        return item_dict


class PonsOliver(Item):
    CRAWLER_NAME = 'pons_oliver'
    SITE_NAME = 'Inmobiliaria Pons Oliver'
    PK = 'url'


class Fotocasa(Item):
    CRAWLER_NAME = 'fotocasa'
    SITE_NAME = 'Fotocasa'
    PK = 'url'


class Idealista(Item):
    CRAWLER = 'idealista'
    SITE_NAME = 'Idealista'
    PK = 'url'
