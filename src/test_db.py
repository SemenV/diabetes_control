from DataBaseExec import *
from datetime import date, timedelta, datetime
import psycopg2
import json
from fsm import FSM

host = '127.0.0.1'
user = 'postgres'
password = 'semen'
db_name = 'uglevodi'


def connect_db():
    connection = psycopg2.connect(
    host = host,
    user = user,
    password = password,
    database = db_name,
    port = 5001
    )
    return connection
    
    
    
db = connect_db()
dbase = DataBaseExec(db)
dt = datetime.now()
print (dt)
z = {"eda" : {},"last" : {},"koef" : ""}



#print(bool(dbase.insertTmpRegIdAlice('тест_только_алисы')))
#db.rollback()
#print(dbase.getNagruzkaPoints('7','szxdfg'))



usr_fsm = FSM()


print(usr_fsm.actDB("сметана",'1',db)[1])