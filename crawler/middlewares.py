# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/spider-middleware.html
from fake_useragent import FakeUserAgent
import logging


class Middleware:
    def process_request(self, request, spider):
        raise NotImplementedError()


class RandomUserAgentMiddleware(Middleware):
    engine = FakeUserAgent()

    def process_request(self, request, spider):
        random_user_agent = self.get_random_user_agent()
        request.headers.setdefault('User-Agent', random_user_agent)
        spider.log(f'Using {random_user_agent}', logging.INFO)

    def get_random_user_agent(self):
        return self.engine.chrome
