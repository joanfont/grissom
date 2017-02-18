import scrapy
from crawler.url_builder import Factory as UrlFactory


class Spider(scrapy.Spider):
    def parse(self, response):
        raise NotImplementedError


class ConfigurableSpider(Spider):
    def start_requests(self):
        urls = UrlFactory.build_urls_for(self.name)
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)
