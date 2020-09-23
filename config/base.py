import os
import socket
from logging.config import dictConfig

BASE_DIR = os.path.dirname(os.path.dirname(__file__))

SECRET_KEY = b"dont_use_this_in_production"

TEMPLATE_FOLDER = "templates"
STATIC_FOLDER = "static"

ALLOWED_HOSTS = [
    "localhost",
    "0.0.0.0",
    "127.0.0.1",
    "gibtesweißesoße.de",
    "gibtesweissesosse.de",
    "xn--gibtesweiesoe-jdbd.de",
    "www.gibtesweißesoße.de",
    "www.gibtesweissesosse.de",
    "www.xn--gibtesweiesoe-jdbd.de",
]

# Add the current host
ALLOWED_HOSTS.append(socket.gethostname())

if os.environ.get("SAUCE_HOST", None) is not None:
    ALLOWED_HOSTS.append(os.environ["SAUCE_HOST"])

dictConfig(
    {
        "version": 1,
        "formatters": {"default": {"format": "%(message)s",}},
        "handlers": {
            "wsgi": {
                "class": "logging.StreamHandler",
                "stream": "ext://flask.logging.wsgi_errors_stream",
                "formatter": "default",
            }
        },
        "root": {"level": "INFO", "handlers": ["wsgi"]},
    }
)

REDIS_CONFIG = {
    "host": os.environ.get("REDIS_HOST", "localhost"),
    "port": os.environ.get("REDIS_PORT", 6379),
    "password": os.environ.get("REDIS_PASSWORD", None),
}

# Celery Settings
CELERY_BROKER_URL = f"redis://{REDIS_CONFIG['host']}:{REDIS_CONFIG['port']}/0"
# Celery does not use the CELERY_ prefix for this config
BROKER_URL = CELERY_BROKER_URL
CELERY_RESULT_BACKEND = CELERY_BROKER_URL

try:
    from .local import *
except ImportError:
    pass
