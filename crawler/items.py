# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Item(scrapy.Item):
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

    notified = scrapy.Field()
    notified_at = scrapy.Field()


class PonsOliverItem(Item):
    SITE_NAME = 'Inmobiliaria Pons Oliver'
    PK = 'url'


class FotocasaItem(Item):
    SITE_NAME = 'Fotocasa'
    PK = 'url'
