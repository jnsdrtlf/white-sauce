#!/bin/bash
export SAUCE_CONFIG=config.prod
celery -A tasks.celery beat --loglevel=info
