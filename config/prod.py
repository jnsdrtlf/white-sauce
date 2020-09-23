import os
from .base import *

SECRET_KEY = os.environ.get("SAUCE_SECRET")
DEBUG = False
TESTING = False
FLASK_ENV = "production"

PREFERRED_URL_SCHEME = "https"
SERVER_NAME = None

# Adjust for server name
# ALLOWED_HOSTS = ['example.org']
