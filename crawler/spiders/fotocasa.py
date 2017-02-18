# -*- coding: utf-8 -*-
import scrapy

from crawler.spiders import ConfigurableSpider


class FotocasaSpider(ConfigurableSpider):
    name = "fotocasa"
    allowed_domains = ["fotocasa.es"]

    def parse(self, response):
        pass
