"""API Entry point."""
from flask import Flask, request, make_response, jsonify
from utils import check_url_index, get_or_create_url_index, index_url, query_url

application = Flask(__name__)

INDEX_FILE = "index.json"
DEFAULT_API_KEY = "YOUR KEY HERE"


@application.route("/check-index", methods=["POST"])
def check_index():
    print(request.json)
    print("Checking index...")
    url = request.json["url"]
    if request.json["apiKey"] != "":
        api_key = request.json["apiKey"]
    else:
        api_key = DEFAULT_API_KEY
    # Check if web page has already been indexed
    response_str = str(check_url_index(url, api_key, INDEX_FILE))
    response = make_response(jsonify(response_str))
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


@application.route("/index-webpage", methods=["POST"])
def index_webpage():
    print("Indexing webpage...")
    url = request.json["url"]
    if request.json["apiKey"] != "":
        api_key = request.json["apiKey"]
    else:
        api_key = DEFAULT_API_KEY
    index_file = get_or_create_url_index(url, INDEX_FILE) + ".json"
    result = index_url(url, index_file, api_key)
    if result:
        response_str = "done"
    else:
        response_str = "error"

    response = make_response(response_str)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


@application.route("/query", methods=["POST"])
def query():
    print("Querying...")
    url = request.json["url"]
    query = request.json["query"]
    if request.json["apiKey"] != "":
        api_key = request.json["apiKey"]
    else:
        api_key = DEFAULT_API_KEY
    # Query indexed web page
    response_str = query_url(url, query, api_key, INDEX_FILE)
    response = make_response(response_str)
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
    response.headers["Access-Control-Allow-Headers"] = "Content-Type"
    return response


cache = {}
if __name__ == "__main__":
    application.run()
