import os

from sauce.tasks import celery
from sauce.tasks.fetch import fetch

config = os.environ.get("SAUCE_CONFIG", "config.dev")
celery.config_from_object(config)
