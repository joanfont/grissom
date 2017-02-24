# -*- coding: utf-8 -*-
import scrapy

from crawler.spiders import Spider
from crawler.items import PonsOliver


class PonsOliverSpider(Spider):
    name = PonsOliver.CRAWLER_NAME
    allowed_domains = ['inmobiliariaesporles.com']
    start_urls = ['http://www.inmobiliariaesporles.com/property-status/alquiler/']

    pk = 'url'

    def parse(self, response):
        items = response.css('article.property-item')
        for item in items:
            yield self.parse_item(item)

        next_page_url = response.css('div.pagination > a.current + a::attr(href)').extract_first()
        if next_page_url:
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_item(self, item):
        title = item.css('h4 > a::text').extract_first().strip()
        url = item.css('h4 > a::attr(href)').extract_first().strip()
        description = item.css('div.detail > p::text').extract_first()
        description = description.strip() if description else None
        price = item.css('div.detail > h5.price::text').extract_first().strip()

        town = 'Esporles'

        return PonsOliver(title=title, url=url, description=description, price=price, town=town)
