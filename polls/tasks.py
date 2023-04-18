import json
import random
import requests

from celery import shared_task
from celery.utils.log import get_task_logger
from celery.signals import task_postrun
from polls.consumers import notify_channel_layer


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


@task_postrun.connect
def task_postrun_handler(task_id, **kwargs):
    """
    When celery task finish, send notification to Django channel_layer.
    Django channel would receive the event and then send it to the web client.
    """

    notify_channel_layer(task_id)
