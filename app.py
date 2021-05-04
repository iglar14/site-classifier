from flask import Flask, request
from flask_cors import CORS
from url_handler import handle_urls

app = Flask(__name__)
CORS(app)


@app.route("/")
def print_hello():
    return "HELLO"


@app.route("/analyze", methods=['GET', 'POST'])
def process_request():
    if request.method == 'GET':
        return "POST request expected", 400
    if request.method == 'POST':
        if 'url' not in request.json:
            return "'url' JSON field is expected", 400

        urls = request.json['url']
        if type(urls) is str:
            # make url list from old-style url parameter, separated by spaces
            urls = urls.split()

        if type(urls) is not list:
            return "url list is expected", 400

        return handle_urls(urls)
