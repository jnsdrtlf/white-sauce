import os
from importlib import import_module

from celery.schedules import crontab

from sauce.tasks import celery
from sauce.tasks.fetch import fetch


config = os.environ.get("SAUCE_CONFIG", "config.dev")
config_module = import_module(config)

celery.conf.update(
    **config_module.CELERY_CONFIG, 
    beat_schedule={
        "fetch-every-morning": {
            "task": "sauce.tasks.fetch.fetch",
            "schedule": crontab(hour=6, minute=0)
        }
    }
)
