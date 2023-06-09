import os

from celery import Celery
from django.conf import settings


# Set the default Django settings module for the celery app.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")


app = Celery("core")

# Read config from Django settings, the 'CELERY' namespace would make celery
# - config keys has 'CELERY' prefix.
app.config_from_object("django.conf.settings", namespace="CELERY")


# Discover and load tasks from all registered Django apps.
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)


@app.task
def divide(x, y):
    # Debugging with rdb
    # from celery.contrib import rdb

    # rdb.set_trace()
    import time

    time.sleep(5)
    return x // y
