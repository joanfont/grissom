class Notifier:
    STATUS_PENDING = 1
    STATUS_NOTIFIED = 2

    def notify(self, item):
        raise NotImplementedError()
