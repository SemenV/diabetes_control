from flask import Flask, request,jsonify
import requests
import json
import os
from fsm import FSM
import pickle

app = Flask(__name__)

@app.route("/", methods=['GET'])
def calc():
    

@app.route("/", methods=['POST'])
def calc_ret():


   
@app.route("/alice", methods=['POST'])
def indexx():

    with open("zapr.json", "r") as my_file:
        zapr_json = my_file.read()

    zapr = json.loads(zapr_json)

    request_data = request.get_json()

    ou = request_data["request"]["original_utterance"]
    if (ou == "ping"):
        zapr["response"]["text"] = "pong"
        return jsonify(zapr)
    
    
    comm = request_data["request"]["command"]
    usr_id = request_data["session"]["user"]["user_id"]
    usr_fsm = 0
    try:
        with open(usr_id + ".pickle", 'rb') as f:
            usr_fsm = data_new = pickle.load(f)
    except:
        usr_fsm = FSM()
        with open(usr_id + ".pickle", 'wb') as f:
            pickle.dump(usr_fsm, f)
    
    
    
    

    if (comm == "помощь"): 
        zapr["response"]["text"] = "Следуй командам и я помогу подсчитать необходимое количество инсулина"
        return jsonify(zapr)
    elif (comm == "что ты умеешь делать"):
        zapr["response"]["text"] = "Я помогу подсчитать необходимое количество инсулина"
        return jsonify(zapr)
    else:
        stroka = usr_fsm.act(comm,usr_id)
        with open(usr_id + ".pickle", 'wb') as f:
            pickle.dump(usr_fsm, f)
        zapr["response"]["text"] = stroka[0]
        return jsonify(zapr)


if __name__ == "__main__":
    app.run(dubug=False, host='0.0.0.0')

