"""
    ingest.py
    Ingests feeds from the config file
    Usage:
    python ingest.py

    GSEARCH_CONFIG_FILE=/path/to/config.json python ingest.py
"""
import config
import json


def main():
    feeds = config.get_ingest_feeds()
    store = config.get_game_store()
    for feed in feeds:
        for game in iter(feed):
            store.add(game)

if __name__ == "__main__":
    main()
