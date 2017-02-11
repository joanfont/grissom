from notifiers.base import Notifier as BaseNotifier
from pushbullet import PushBullet


class Notifier(BaseNotifier):

    def __init__(self, api_key):
        self.client = PushBullet(api_key)

    def notify(self, item):
        site_name = item.SITE_NAME
        title = f'New property in {site_name}'
        link = item.get('url')
        self.client.push_link(title, link)
