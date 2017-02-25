# -*- coding: utf-8 -*-
import scrapy

from crawler.items import Idealista
from crawler.spiders import ConfigurableSpider


class IdealistaSpider(ConfigurableSpider):
    name = Idealista.CRAWLER_NAME
    allowed_domains = ['idealista.com']

    def parse(self, response):
        items = response.css('div.items-container > article:not([class])')
        zone = response.css('div.breadcrumb-geo > ul > li.current-level > span::text').extract_first().strip()

        for item in items:
            yield self.parse_item(item, zone)

        next_page_path = response.css(
            'div.pagination > ul > li.selected + li > a::attr(href)'
        ).extract_first()

        if next_page_path:
            next_page_url = self.url_builder.append_to_base(next_page_path)
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_item(self, item, zone):
        info_container = item.css('div.item-info-container')

        title = info_container.css('a.item-link::attr(title)').extract_first().strip()
        url = info_container.css('a.item-link::attr(href)').extract_first().strip()
        url = self.url_builder.append_to_base(url)

        description = info_container.css('p.item-description::text').extract_first()
        description = description.strip() if description else None
        price = info_container.css('div.price-row > span.item-price::text').extract_first().strip()

        return Idealista(title=title, url=url, description=description, price=price, town=zone)
