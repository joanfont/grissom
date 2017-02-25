from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

from async.celery import app


@app.task
def crawl(spider_name):
    do_crawl(spider_name)


def do_crawl(spider_name):
    process = CrawlerProcess(get_project_settings())
    process.crawl(spider_name)
    process.start()
