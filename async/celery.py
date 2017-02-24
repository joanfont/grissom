from celery import Celery

app = Celery(
    'tasks',
    broker='amqp://guest@rabbit//',
    backend='rpc://',
    include=['async.tasks']
)

