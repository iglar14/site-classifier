from flask import Flask, jsonify,request,make_response,url_for,redirect
from flask_cors import CORS
from json import dumps
from requests import post
import pickle
from url_handler import handle_url

nhash = 'analyze'

app = Flask(__name__)
CORS(app)

@app.route("/")
def PrintHello():
    return "HELLO"

@app.route("/"+str(nhash), methods=['GET', 'POST'])

def process_request():
    if request.method == 'GET':
        return "Wrong type of request!"
    if request.method == 'POST':
        url = request.json['url']
        return handle_url(url)
        