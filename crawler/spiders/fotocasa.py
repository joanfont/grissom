# -*- coding: utf-8 -*-
import scrapy

from crawler.items import Fotocasa
from crawler.spiders import ConfigurableSpider


class FotocasaSpider(ConfigurableSpider):
    name = Fotocasa.CRAWLER_NAME
    allowed_domains = ['fotocasa.es']

    def parse(self, response):
        items = response.css('div.re-Card')
        zone = response.css(
            'ol.re-Breadcrumb-links > li.re-Breadcrumb-item:last-child > span::text'
        ).extract_first().strip()

        for item in items:
            yield self.parse_item(zone, item)

        next_page_path = response.css(
            'ul.sui-Pagination-list > li.sui-Pagination-item--selected + li > a::attr(href)'
        ).extract_first()

        if next_page_path:
            next_page_path = next_page_path
            next_page_url = self.url_builder.append_to_base(next_page_path)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_item(self, zone, item):
        title = item.css('a.re-Card-title::text').extract_first().strip()
        url = item.css('a.re-Card-title::attr(href)').extract_first().strip()
        description = item.css('span.re-Card-description::text').extract_first()
        description = description.strip() if description else None
        price = item.css('span.re-Card-price > span::text').extract_first().strip()

        return Fotocasa(title=title, url=url, description=description, price=price, town=zone)
