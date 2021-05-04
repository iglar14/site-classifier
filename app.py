from flask import Flask, request
from flask_cors import CORS
from url_handler import handle_url

app = Flask(__name__)
CORS(app)


@app.route("/")
def print_hello():
    return "HELLO"


@app.route("/analyze", methods=['GET', 'POST'])
def process_request():
    if request.method == 'GET':
        return "Wrong type of request!"
    if request.method == 'POST':
        url = request.json['url']
        return handle_url(url)
