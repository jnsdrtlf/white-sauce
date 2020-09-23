export SAUCE_CONFIG=config.prod
alembic upgrade head
uwsgi --ini etc/uwsgi.ini