"""
    config.py

    Provides an interface to get values from the config file.

    Example:
    config.get("game_store.data_dir") -> data/games
"""
import json
import os
from gamesearch.store import GameStore
from importlib import import_module

config_file = os.getenv("GSEARCH_CONFIG_FILE", "config.json")
with open(config_file, "r") as fp:
    config = json.load(fp)


def get(key):
    """
    Returns a key from the config file using dot notation.
    get("feeds.giantbomb")
    If the key does not exists, it returns None
    """
    keys = key.split(".")
    value = config
    while len(keys) > 0:
        if not value:
            break
        k = keys.pop(0)
        value = value.get(k)
    return value


def get_game_store():
    """
    Returns an instance of the GameStore using the config file
    """
    return GameStore(**get('game_store'))


def import_feed(config):
    """
    Imports a feed module.class path using the config dictionary and returns the feed instance
    """
    try:
        p, m = config["path"].rsplit('.', 1)
        mod = import_module(p)
        met = getattr(mod, m)
    except AttributeError:
        raise Exception("Invalid feed path: %s" % config["path"])
    return met(**config.get("params", {}))


def get_ingest_feeds():
    """
    Returns feeds to ingest
    """
    feed_configs = [config for feed_id, config in get("feeds").items() if config.get("ingest")]
    return [import_feed(config) for config in feed_configs]
