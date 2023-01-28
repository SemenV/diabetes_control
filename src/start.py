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
    
    
    if (fsm.act("диабет")[0] == 1):
        print("Команда недоступна")
    
    
    
    
    
    
    
    
    
    
    
    
    
    if comm == "диабет":
        with open("ses.json", "w") as my_file:
            my_file.write(json.dumps(z))
            zapr["response"]["text"] = "перечислите продукты"
            return jsonify(zapr)
            
            
            
            
            
            
            
    if comm == "подсчитать":
        with open("ses.json", "r") as my_file:
            ses_json = json.loads(my_file.read())
        sum_val = 0
        for key_g, values_g in ses_json["eda"].items():
            sum_val = sum_val + values_g
        zapr["response"]["text"] = sum_val
        return jsonify(zapr)
            
    else:
        r = requests.get("https://ru-ru.openfoodfacts.org/category/" + comm + "/1.json")
        ugl = -1 
        i = 0;
        while ugl < 0: 
            try: r.json()["products"][i]["nutriments"]["carbohydrates"]
            except:
                i = i + 1
                continue
            else:
                ugl = r.json()["products"][i]["nutriments"]["carbohydrates"]
                
                
        with open("ses.json", "r") as my_file:
            ses_json = json.loads(my_file.read())
            
        ses_json["eda"][comm] = ugl
        
        with open("ses.json", "w") as my_file:
            my_file.write(json.dumps(ses_json))
        
        
        zapr["response"]["text"] = ugl
        return jsonify(zapr)
    
if __name__ == "__main__":
    app.run(dubug=False, host='0.0.0.0')

