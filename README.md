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

