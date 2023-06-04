from flask import Flask, request,jsonify , render_template, flash, session,url_for,redirect,g
import psycopg2
import requests
import json
import os
from datetime import date, timedelta, datetime
from fsm import FSM
from DataBaseExec import *
import pickle
from  splineDeriv import * 

host = 'host.docker.internal'
user = 'postgres'
password = 'semen'
db_name = 'uglevodi'




def connect_db():
    connection = psycopg2.connect(
    host = host,
    user = user,
    password = password,
    database = db_name,
    )
    return connection
    
def get_database():
    if not hasattr(g, 'link_db'):
        g.link_db = connect_db()
    return g.link_db



app = Flask(__name__)
app.config["SECRET_KEY"] = 'wqeqweqew'
app.debug = True


@app.teardown_appcontext
def close_db(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()

@app.route("/login", methods=['POST','GET'])
def tlog():
    if request.method == "POST":
        db = get_database()
        dbase = DataBaseExec(db)
        IDDB = dbase.getIdByLoginPsw(request.form['username'],request.form['password'])
        session['userIdLogged'] = IDDB[0][0]
        dt = datetime.now()
        flash(dbase.getDayMenu(session['userIdLogged'],dt)    )
            
    if 'userIdLogged' in session:
        return redirect(url_for('profile_day',day = '20.05.2023'))
 
      
      
    return render_template("login.html")


@app.route("/profile/<day>", methods=['POST','GET'])
def profile_day(day):

    if 'userIdLogged' in session:
        return render_template("profile.html",day = day)
    else:
        return redirect(url_for('tlog'))
    
    
@app.route("/logout", methods=['POST','GET'])
def logout():
    session.clear()
    return redirect(url_for('tlog'))

@app.route("/", methods=['POST','GET'])
def send_to_calc_ret():
    return redirect(url_for('calc_ret',nagruzka = "hod"))


@app.route("/nagr/<nagruzka>", methods=['POST','GET'])
def calc_ret(nagruzka):
    if request.method == "GET":
        return render_template("calc.html",nagruzka = nagruzka )

    session['tmp_values'] = ""
    session['main_values'] = ""
    session['counter'] = ""
    
    db = get_database()
    if request.method == "POST":
        counter = request.form['counter']
        session['counter'] = counter
        main_values = []
        tmp_values = []
        A = []
        B = []
        proizv = []
        for i in range(int(counter)):
            i = i + 1;
            x = float(request.form['x' + str(i)])
            A.append(x)
            main_values.append(x)
            y = float(request.form['y' + str(i)])
            B.append(y)
            main_values.append(y)
            yp = float(request.form['yp' + str(i)])
            proizv.append(yp)
            main_values.append(yp)
            tmp_values.append({"x": x, "y" : y})
        
        
        all_values = get_spl_prepered(A,B,proizv,0.1)
            

        session['tmp_values'] = json.dumps(all_values)
        session['main_values'] = main_values
        session.modified = True
        flash(' '.join([str(elem) for elem in main_values]))


    return render_template("calc.html", nagruzka = nagruzka)


   
@app.route("/alice", methods=['GET','POST'])
def indexx():
    db = get_database()
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
            usr_fsm  = pickle.load(f)
    except:
        usr_fsm = FSM()
        strokaStage = usr_fsm.act("начало",usr_id,db)
        with open(usr_id + ".pickle", 'wb') as f:
            pickle.dump(usr_fsm, f)
    
    
    
    

    if (comm == "помощь"): 
        zapr["response"]["text"] = "Следуй командам и я помогу подсчитать необходимое количество инсулина"
        return jsonify(zapr)
    elif (comm == "что ты умеешь делать"):
        zapr["response"]["text"] = "Я помогу подсчитать необходимое количество инсулина"
        return jsonify(zapr)
    else:
    
    

        stroka = usr_fsm.act(comm,usr_id,db)
        with open(usr_id + ".pickle", 'wb') as f:
            pickle.dump(usr_fsm, f)
        zapr["response"]["text"] = stroka[0]
        return jsonify(zapr)


if __name__ == "__main__":
    app.run(dubug=True, host='0.0.0.0')

