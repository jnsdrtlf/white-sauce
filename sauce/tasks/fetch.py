import os
from importlib import import_module
from io import StringIO
from datetime import date, timedelta

import requests
from lxml import etree
from redis import Redis

from sauce.tasks import celery
from sauce.util.identifier import SAUCE_IDENTIFIER


@celery.task
def fetch():
    config = os.environ.get("SAUCE_CONFIG", "config.dev")
    config_module = import_module(config)

    redis_config = getattr(config_module, "REDIS_CONFIG", None)
    if redis_config == None:
        raise RuntimeError("Unable to find REDIS_CONFIG")
    redis = Redis(**redis_config)

    url = "https://www.studentenwerk.uni-heidelberg.de/de/node/135"
    response = requests.get(url)
    htmlparser = etree.HTMLParser()
    tree = etree.fromstring(response.text, htmlparser)

    table = tree.xpath("//h2[text()='Mensa Im Neuenheimer Feld 304']/following-sibling::div//div[contains(@class, 'mensa-carousel')]//div[contains(@class, 'item')]//h4/following-sibling::table[1]")[0]
    text = " ".join([n.strip() for n in table.itertext()]).strip().lower()
    is_it_in_there = 0

    for sauce in SAUCE_IDENTIFIER:
        if sauce.lower() in text:
            is_it_in_there = 1
            break

    today = date.today()
    
    if today.weekday() >= 5:
        is_it_in_there = 0
        
    old_date = redis.get("sauce_last_date")
    if old_date is None:
        old_date = (today - timedelta(days=1)).isoformat()
    if isinstance(old_date, bytes):
        old_date = old_date.decode()
    if today > date.fromisoformat(old_date):
        tot = redis.get("sauce_total")
        if tot is None:
            tot = 0
        tot += is_it_in_there
        redis.set("sauce_total", tot)

    redis.set("sauce_current_status", is_it_in_there)
    redis.set("sauce_last_date", today.isoformat())
