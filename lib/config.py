from decouple import config

CELERY_USER = config('CELERY_USER', default='guest')
CELERY_HOST = config('CELERY_HOST', default='rabbit')

CELERY_DSN = 'amqp://{celery_user}@{celery_host}//'.format(
    celery_user=CELERY_USER,
    celery_host=CELERY_HOST
)

MONGO_HOST = config('MONGO_HOST', default='mongo')
MONGO_PORT = config('MONGO_PORT', default=27017, cast=int)
MONGO_DATABASE = config('MONGO_DATABASE', default='crawlers')

PUSHBULLET_API_KEY = config('PUSHBULLET_API_KEY')
