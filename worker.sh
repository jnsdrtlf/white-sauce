#!/bin/bash
export SAUCE_CONFIG=config.prod
celery worker -A tasks.celery --loglevel=info
