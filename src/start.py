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
    return redirect(url_for('tlog'))



@app.route("/new_subspline_nagr", methods=['POST','GET'])
def new_nagr():
    if 'userIdLogged' in session:
        session['tmp_values'] = ""
        session['main_values'] = ""
        session['counter'] = 0
        
        if request.method == "GET":
            return render_template("new_subspline_nagr_html.html")


        if request.method == "POST":
            counter = int(request.form.get('counter'))
            session['counter'] = counter
            main_values = []
            A = []
            B = []
            proizv = []
            for i in range(counter):
                x = float(request.form.get('x' + str(i)))
                A.append(x)
                main_values.append(x)
                y = float(request.form.get('y' + str(i)))
                B.append(y)
                main_values.append(y)
                yp = float(request.form.get('yp' + str(i)))
                proizv.append(yp)
                main_values.append(yp)

            
            
            all_values = get_spl_prepered(A,B,proizv,0.1)
                

            session['tmp_values'] = json.dumps(all_values)
            session['main_values'] = main_values
            session.modified = True
            flash(' '.join([str(elem) for elem in main_values]))
            if (request.form.get("savebtn") != None):
                db = get_database()
                dbase = DataBaseExec(db)
                userIdLogged = session['userIdLogged']
                nazvanie = request.form['nazvanie']
                dbase.setNagruzka(str(userIdLogged),nazvanie,json.dumps(main_values, ensure_ascii=False), 'subspline')

        return render_template("new_subspline_nagr_html.html")
            
    else:
        return redirect(url_for('tlog'))


@app.route("/show_nagr", methods=['POST','GET'])
def calc_ret():
    if 'userIdLogged' in session:
        session['tmp_values'] = ""
        session['main_values'] = ""
        session['counter'] = ""
        userIdLogged = str(session['userIdLogged'])
        db = get_database()
        dbase = DataBaseExec(db)
        
        

            

        
        nazvanie = request.form.get('select_nagruzka')
        if (nazvanie == None):
            name = dbase.getNagruzkaNames(userIdLogged)[0][0]
            session['nagruzka'] = name
        else:
            session['nagruzka'] = nazvanie            
        finalNagruzka = session['nagruzka']
    
        session['allNagruzki'] = dbase.getNagruzkaNames(userIdLogged)
    
        points = json.loads(dbase.getNagruzkaPoints(userIdLogged,finalNagruzka)[0][0])
        
        all_values = get_spl_prepered_two(points,0.1)
        
        session['tmp_values'] = json.dumps(all_values)
    
    
    
        return render_template("show_nagr_html.html" )


        
    else:
        return redirect(url_for('tlog'))
        

   
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

    
 
    
    
    

    if (comm == "помощь"): 
        zapr["response"]["text"] = "Следуй командам и я помогу подсчитать необходимое количество инсулина"
        return jsonify(zapr)
    elif (comm == "что ты умеешь делать"):
        zapr["response"]["text"] = "Я помогу подсчитать необходимое количество инсулина"
        return jsonify(zapr)
    else:
    
    
        usr_fsm = FSM()
        stroka = usr_fsm.actDB(comm,usr_id,db)

        zapr["response"]["text"] = stroka[1]
        return jsonify(zapr)


if __name__ == "__main__":
    app.run(dubug=True, host='0.0.0.0')

