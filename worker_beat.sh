#!/bin/bash
export SAUCE_CONFIG=config.prod
celery --app tasks.celery beat