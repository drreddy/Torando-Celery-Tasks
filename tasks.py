import os
import time
from datetime import datetime

from celery import Celery


celery = Celery("tasks", broker="amqp://guest:guest@localhost:5672//")
celery.conf.CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'amqp')


@celery.task(bind=True)
def sleep(self,seconds):
    startime = datetime.now().isoformat()
    time.sleep(float(seconds))
    endtime = datetime.now().isoformat()
    return [self.request.id, startime, endtime]

@celery.task
def error(msg):
    raise Exception(msg)


if __name__ == "__main__":
    celery.start()