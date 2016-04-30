# gamesearch

## Dependencies
Flask is needed to run the REST API. 

`
pip install flask
`

## Data Structures

The search by name is done using an inverted index, see `gamesearch/index.py`. Each game name is split into tokens, each token contains a list of (game_id, position) tuples. For each token, a list of game_ids and position is saved in a file in data/games/index directory. The game ids are in ascending order.

To query compound words, I intersect the game_ids set for each token. See `gamesearch/index.py intersect()` I use an algorithm that takes advantage of the ascending order of game ids. If a token file has 1M entries, it will not iterate them all, it will only iterate what's neccessary. An improvement can be made by sorting tokens by increasing frequency order, to make the least amount of work while intersecting.

The inverted index is file based, so it does not require to hold anything in memory. In addition, it allows the API to return new results without any downtime.

## Ingest

To ingest the feeds, run the following command:

`python ingest.py`

This will look for feeds marked as `ingest:true` in the config file.

## Query

### REST API
The following command will start a server at port 5000

`python app.py`

Go to `http://localhost:5000/version` to check that is working correctly.

To query, make the following request:

`GET /search?query={query}`

### Examples

`GET /search?query=mario+party`

## Config File

The default location for the config file is `config.json`. If you want to change this, use `GSEARCH_CONFIG_FILE` environment variable.

`GSEARCH_CONFIG_FILE=/path/to/config.json python ingest.py`

### feeds

The config file contains the available feeds. Each feed requires at least the `path` key. 

The `path` key is the module.class path to import from python. This allow us to install third party feeds using pip, and just reference them in the config file. 

The `params` path is a dictionary of arguments to send to the feed constructor.

`ingest` is a boolean that specifies if this feed should be ingested or not when running `ingest.py`



