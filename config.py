import json
import os
from gamesearch.store import GameStore
from importlib import import_module

config_file = os.getenv("GSEARCH_CONFIG_FILE", "config.json")
with open(config_file, "r") as fp:
    config = json.load(fp)


def get(key):
    keys = key.split(".")
    value = config
    while len(keys) > 0:
        k = keys.pop(0)
        value = value[k]
    return value


def get_game_store():
    return GameStore(**get('game_store'))


def import_feed(config):
    try:
        p, m = config["path"].rsplit('.', 1)
        mod = import_module(p)
        met = getattr(mod, m)
    except AttributeError:
        raise Exception("Invalid feed path: %s" % config["path"])
    return met(**config.get("params", {}))


def get_ingest_feeds():
    feed_configs = [config for feed_id, config in get("feeds").items() if config.get("ingest")]
    return [import_feed(config) for config in feed_configs]
