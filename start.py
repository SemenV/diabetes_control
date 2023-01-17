from flask import Flask, jsonify

app = Flask(__name__)



testt = {
    
    "response": {
      "text": "Привет - это ответ",
      "end_session": "false"
    },
    "version": "1.0"
 
}

@app.route("/", methods=['GET'])
def index():
    return jsonify(testt)
    
@app.route("/", methods=['POST'])
def indexx():
    return jsonify(testt)
    
if __name__ == "__main__":
    app.run(dubug=False, host='0.0.0.0')

