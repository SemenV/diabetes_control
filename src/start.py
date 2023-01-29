from flask import Flask, request,jsonify
import requests
import json
import os
from fsm import FSM

fsm = FSM()

app = Flask(__name__)


   
@app.route("/", methods=['POST'])
def indexx():

    with open("zapr.json", "r") as my_file:
        zapr_json = my_file.read()

    zapr = json.loads(zapr_json)

    request_data = request.get_json()
    comm = request_data["request"]["command"]
    
    stroka = fsm.act(comm)
    zapr["response"]["text"] = stroka
    return jsonify(zapr)
    

if __name__ == "__main__":
    app.run(dubug=False, host='0.0.0.0')

