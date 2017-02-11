import scrapy


class Spider(scrapy.Spider):
    pk = None

    def parse(self, response):
        raise NotImplementedError
