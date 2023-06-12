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
from linear_inter import *
from spl_points_prepared import *

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
        

            
    if 'userIdLogged' in session:
        return redirect(url_for('profile_day'))
 
      
      
    return render_template("login.html")



@app.route("/user_eda_save", methods=['POST','GET'])
def user_eda_save():
    db = get_database()
    dbase = DataBaseExec(db)
    prodAddName = request.form.get('prodAddName')
    prodAddParam = request.form.get('prodAddParam')
    dbase.setFoodUserEda(session['userIdLogged'],prodAddName,prodAddParam)
    return redirect(url_for('user_eda'))   
    
    

@app.route("/user_eda", methods=['POST','GET'])
def user_eda():
    db = get_database()
    dbase = DataBaseExec(db)
    if request.method == "POST":
            prodToRem = request.form.get('removeProd')
            dbase.romoveFromUserEda(session['userIdLogged'],prodToRem)

    session['user_food'] = dbase.getAllUserEdaById(session['userIdLogged'])
    return render_template("user_eda_html.html")
    


@app.route("/profile", methods=['POST','GET'])
def profile_day():
    if 'userIdLogged' in session:
        if request.method == "GET":
            session['day'] = datetime.now().strftime('%Y-%m-%d')
        if request.method == "POST":
            session['day'] = request.form.get("start")
        db = get_database()
        dbase = DataBaseExec(db)
        res = dbase.getDayMenu(session['userIdLogged'],datetime.strptime(session['day'] , '%Y-%m-%d'))
        
        resPy = []
        for i in res:
            elem = []
            elem.append(i[0])
            elem.append(json.loads(i[1]))
            resPy.append(elem)
        
        session['dayMenu'] = resPy
        flash(res)
    
        return render_template("profile.html")
    else:
        return redirect(url_for('tlog'))
    
    
@app.route("/logout", methods=['POST','GET'])
def logout():
    session.clear()
    return redirect(url_for('tlog'))

@app.route("/", methods=['POST','GET'])
def send_to_calc_ret():
    return redirect(url_for('tlog'))
    
@app.route("/admin_save", methods=['POST'])
def admin_save():
    db = get_database()
    dbase = DataBaseExec(db)
    role = dbase.getUserRole(session['userIdLogged'])[0][0]
    if (role == 'admin'):
        prodAddName = request.form.get('prodAddName')
        prodAddParam = request.form.get('prodAddParam')
        dbase.setFoodLocalFood(prodAddName,prodAddParam)
    return redirect(url_for('admin_panel')) 

@app.route("/admin", methods=['POST','GET'])
def admin_panel():
    if 'userIdLogged' in session:
        db = get_database()
        dbase = DataBaseExec(db)
        role = dbase.getUserRole(session['userIdLogged'])[0][0]
        if (role == 'admin'):
            if request.method == "POST":
                prodToRem = request.form.get('removeProd')
                dbase.romoveFromLocalFood(prodToRem)
            session['all_food'] = dbase.getAllLocalFood()
            return render_template("admin_panal.html")


@app.route("/new_linear_nagr", methods=['POST','GET'])
def new_linear_nagr():
    if 'userIdLogged' in session:
        session['tmp_values'] = ""
        session['main_values'] = ""
        main_values = []
        
        if request.method == "POST":
            x = float(request.form.get('x'))
            main_values.append(x)
            y = float(request.form.get('y'))
            main_values.append(y)
            tg = y/x
            all_values = get_linear_prepered(tg,0.2)
            session['tmp_values'] = json.dumps(all_values)
            session['main_values'] = main_values
            session['main_values_json'] = json.dumps(get_main_linear_point(main_values))
            if (request.form.get("savebtn") != None):
                db = get_database()
                dbase = DataBaseExec(db)
                userIdLogged = session['userIdLogged']
                nazvanie = request.form['nazvanie']
                dbase.setNagruzka(str(userIdLogged),nazvanie,json.dumps(tg, ensure_ascii=False), 'linear')
            
        return render_template("new_linear_nagr_html.html")
    else:
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
            session['main_values_json'] = json.dumps(get_all_main_spl_prepared_two(main_values))
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
        
        typeNagr = dbase.getNagrAndTypeById(session['userIdLogged'],finalNagruzka)[0][1]
        all_values = []
        if (typeNagr == 'subspline'):
            all_values = get_spl_prepered_two(points,0.1)
        else:
            all_values = get_linear_prepered(points,0.2)
            
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
    app.run(dubug=True, host='host.docker.internal')

