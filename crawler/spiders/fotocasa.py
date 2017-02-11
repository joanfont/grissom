# -*- coding: utf-8 -*-
import scrapy


class FotocasaSpider(scrapy.Spider):
    name = "fotocasa"
    allowed_domains = ["fotocasa.es"]
    start_urls = ['http://fotocasa.es/']

    def parse(self, response):
        pass
