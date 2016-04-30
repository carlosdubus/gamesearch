# gamesearch

## Dependencies
Flask is needed to run the REST API. 

`
pip install flask
`

## Ingest

To ingest the feeds, run the following command:

`python ingest.py`

This will look for feeds marked as `ingest:true` in the config file.

## Query

### REST API
The following command will start a server in port 5000

`python app.py`

Go to `http://localhost:5000/version` to check that is working correctly.

To issue a query make the following request:

`GET /search?query={query}`

### Examples

`GET /search?query=mario+party`

## Config File

The default location for the config file is `config.json`. If you want to change this, use `GSEARCH_CONFIG_FILE` environment variable.

`GSEARCH_CONFIG_FILE=/path/to/config.json python ingest.py`

### feeds

The config file contains the available feeds. Each feed require at least the `path` key. The `path` key is the module.class path to import from python. This allows to install third party feeds using pip, and just reference them in the config file. 

The `params` path is a dictionary of arguments to send to the feed constructor.

`ingest` is a boolean that specifies if this feed should be ingested or not when running `ingest.py`



