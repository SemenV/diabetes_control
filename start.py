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
    zapr["response"]["text"] = r.json()["products"][1]["nutriments"]["carbohydrates"]
    return jsonify(zapr)
    
if __name__ == "__main__":
    app.run(dubug=False, host='0.0.0.0')

