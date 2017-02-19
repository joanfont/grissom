import scrapy
from crawler.url_builder import Factory as UrlBuilderFactory


class Spider(scrapy.Spider):
    def parse(self, response):
        raise NotImplementedError


class ConfigurableSpider(Spider):
    def __init__(self, name=None, **kwargs):
        self.url_builder = UrlBuilderFactory.build(self.name)
        super().__init__(name, **kwargs)

    def start_requests(self):
        urls = self.url_builder.generate()
        for url in urls:
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        raise NotImplementedError()
