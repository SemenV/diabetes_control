from flask import Flask, request,jsonify
import requests
import json

app = Flask(__name__)

with open("zapr.json", "r") as my_file:
    zapr_json = my_file.read()

zapr = json.loads(zapr_json)
   
@app.route("/", methods=['POST'])
def indexx():
    request_data = request.get_json()
    comm = request_data["request"]["command"]
    
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
    
    zapr["response"]["text"] = ugl
    return jsonify(zapr)
    
if __name__ == "__main__":
    app.run(dubug=False, host='0.0.0.0')

