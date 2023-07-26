from flask import Flask, make_response, request
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

url = "https://bahnar.dscilab.site:20007/speak/vi_ba"
headers = {
          'Content-Type': 'application/json'
          }

@app.route('/speak', methods=['POST'])
def speak():
    payload = json.dumps({
          "text": request.get_json()["text"]
          "gender": request.get_json()["gender"]
          "region": request.get_json()["region"]
          })
    response = requests.request("POST", url, headers=headers, data=payload)

    return make_response({"speech": response.json()["speech"],"speech_fm": response.json()["speech_fm"]})