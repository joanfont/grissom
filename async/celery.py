from celery import Celery

from async import periodic
from lib import config

app = Celery(
    'tasks',
    broker=config.CELERY_DSN,
    backend='rpc://',
    include=['async.notifiers', 'async.crawlers']
)

app.conf.beat_schedule = periodic.get_config()
app.conf.worker_max_tasks_per_child = 1