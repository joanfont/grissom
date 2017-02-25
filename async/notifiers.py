from datetime import datetime

from async.celery import app
from lib import config
from lib import utils
from notifiers import PushBulletNotifier


@app.task()
def pushbullet(item):
    saved_item = fetch_item(item)
    if saved_item.get('notified', PushBulletNotifier.STATUS_NOTIFIED) == PushBulletNotifier.STATUS_NOTIFIED:
        return

    pushbullet_api_key = config.PUSHBULLET_API_KEY
    notifier = PushBulletNotifier(pushbullet_api_key)
    notifier.notify(saved_item)

    update_notified_status(saved_item)


def fetch_item(item):
    pk_name = item.get('pk')
    pk_value = item.get(pk_name)
    crawler = item.get('crawler')

    with utils.make_mongo_client() as mongo:
        collection = mongo[crawler]
        saved = collection.find_one({pk_name: pk_value})

    return saved


def update_notified_status(saved_item):
    crawler = saved_item.get('crawler')

    with utils.make_mongo_client() as mongo:
        collection = mongo[crawler]

        collection.update_one({
            '_id': saved_item.get('_id')
        }, {
            '$set': {
                'notified': PushBulletNotifier.STATUS_NOTIFIED,
                'notified_at': datetime.now()
            }
        })
