from flask import Flask, request,jsonify

app = Flask(__name__)



testt = {
    
    "response": {
      "text": "Привет - это ответ",
      "end_session": "false"
    },
    "version": "1.0"
 
}

   
@app.route("/", methods=['POST'])
def indexx():
    request_data = request.get_json()
    comm = request_data["request"]["command"]
    testt["response"]["text"] = comm
    return jsonify(testt)
    
if __name__ == "__main__":
    app.run(dubug=False, host='0.0.0.0')

