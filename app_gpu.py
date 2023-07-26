from flask import Flask, make_response, request
from flask_cors import CORS
import requests
import json

app = Flask(__name__)
CORS(app)

url = "https://bahnar.dscilab.site:20007/speak/vi_ba"
url_v2 = "https://bahnar.dscilab.site:20007/speak/vi_ba_v2"
headers = {
          'Content-Type': 'application/json'
          }

@app.route('/speak', methods=['POST'])
def speak():
    payload = json.dumps({
          "text": request.get_json()["text"],
          "gender": request.get_json()["gender"],
          "region": request.get_json()["region"]
          })
    response = requests.request("POST", url, headers=headers, data=payload)

    return make_response({"speech": response.json()["speech"],"speech_fm": response.json()["speech_fm"]})

@app.route('/speak_v2', methods=['POST'])
def speak_v2():
      payload = json.dumps({
            "text": request.get_json()["text"],
            "gender": request.get_json()["gender"],
            "region": request.get_json()["region"]
            })
      response = requests.request("POST", url_v2, headers=headers, data=payload)
      response = json.loads(response.json())
      return make_response(response)

@app.route('/delete_v2', methods=['POST'])
def delete_v2():
      payload = json.dumps({
            "urls": request.get_json()["urls"]
            })
      
      response = requests.request("DELETE", url_v2, headers=headers, data=payload)
      if response.status_code == 200:
            return make_response({"message": "Delete successfully"})
      else:
            return make_response({"message": "Delete failed"})