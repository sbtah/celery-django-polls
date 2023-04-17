import json
import random
import requests

from celery import shared_task
from celery.utils.log import get_task_logger


logger = get_task_logger(__name__)


@shared_task()
def sample_task(email):
    from polls.views import api_call

    api_call(email)


@shared_task(bind=True)
def task_process_notification(self):
    try:
        if not random.choice([0, 1]):
            # Mimic random error
            raise Exception()
        requests.post("https://httpbin.org/delay/5")
    except Exception as e:
        logger.error("Esception raised. Retrying in 5 seconds ...")
        raise self.retry(exc=e, countdown=5)
