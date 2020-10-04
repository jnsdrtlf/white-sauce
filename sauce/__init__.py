import os
from importlib import import_module

import click
from flask import Flask, render_template
from flask.cli import FlaskGroup
from redis import Redis

from sauce.util.host_middleware import host_middleware
from sauce.tasks import celery
from sauce.tasks.fetch import fetch


EMPTY = ["", None, (), [], {}, b""]


def create_app(name="sauce", config=None):
    if config is None:
        config = os.environ.get("SAUCE_CONFIG", "config.dev")

    # Import the configuration object
    config_module = import_module(config)
    # Only initialize sentry if in production and SENTRY_DSN is set
    _env = os.environ.get("FLASK_ENV", "development")

    app = Flask(name, instance_relative_config=True)

    app.config.from_object(config_module)
    app.static_url_path = app.config.get("STATIC_FOLDER")
    app.static_folder = os.path.join(app.root_path, app.static_url_path)

    host_middleware(app)

    redis = Redis(**app.config["REDIS_CONFIG"])
    celery.conf.update(
        **config_module.CELERY_CONFIG,
    )

    fetch.delay()

    @app.route("/", methods=["GET"])
    def index():
        res = redis.get("sauce_current_status")
        total = redis.get("sauce_total")
        if total in EMPTY:
            total = b"0"
        total = total.decode()
        if tasks in EMPTY:
            res = False
        else:
            try:
                res = bool(int(res))
            except ValueError:
                res = False

        visitors = redis.get("sauce_visit")
        if visitors in EMPTY:
            visitors = b"0"
        visitors = int(visitors)
        visitors += 1
        redis.set("sauce_visit", visitors)

        return render_template("index.html", sauce=res, total=total)

    @app.route("/imprint", methods=["GET"])
    def impressum():
        return render_template("impressum.html")

    return app


@click.group(cls=FlaskGroup, create_app=create_app)
def cli():
    """
    Sauce Command Line Interface

    Uses the default ``FlaskGroup`` to provide the default flask
    interface with commands such as ``run``, ``shell``, etc.
    """
    pass
