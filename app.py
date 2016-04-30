from flask import Flask, jsonify, request
import config
import json
app = Flask(__name__)
gamestore = config.get_game_store()

APP_VERSION = "0.01"


@app.route("/search")
def search():
    query = request.args.get('query')
    results = gamestore.find_by_name(query)
    return jsonify(results=[g.__dict__ for g in results])


@app.route("/version")
def version():
    return jsonify(version=APP_VERSION)

if __name__ == "__main__":
    app.run()
