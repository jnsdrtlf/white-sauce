import os

from celery.schedules import crontab

from sauce.tasks import celery
from sauce.tasks.fetch import fetch


config = os.environ.get("SAUCE_CONFIG", "config.dev")
celery.config_from_object(config)

celery.conf.CELERYBEAT_SCHEDULE = {
    "fetch-every-morning": {
        "task": "sauce.tasks.fetch.fetch",
        "schedule": crontab(hour=6, minute=0)
    }
}
