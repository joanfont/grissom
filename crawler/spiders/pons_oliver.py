# -*- coding: utf-8 -*-
import scrapy

from crawler.spiders import Spider
from crawler.items import PonsOliverItem


class PonsOliverSpider(Spider):
    name = "pons_oliver"
    allowed_domains = ["inmobiliariaesporles.com"]
    start_urls = ['http://www.inmobiliariaesporles.com/property-status/alquiler/']

    pk = 'url'

    def parse(self, response):
        items = response.css('article.property-item')
        for item in items:
            yield self.parse_item(item)

    def parse_item(self, item):
        title = item.css('h4 > a::text').extract_first().strip()
        url = item.css('h4 > a::attr(href)').extract_first().strip()
        description = item.css('div.detail > p::text').extract_first()
        description = description.strip() if description else None
        price = item.css('div.detail > h5.price::text').extract_first().strip()

        return PonsOliverItem(title=title, url=url, description=description, price=price)
