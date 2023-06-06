from DataBaseExec import *
from datetime import date, timedelta, datetime
import psycopg2
import json
from fsm import *
import ast
from pytz import timezone

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

#qwe = Node9("\d*\.*\d*","Скажите время нагрузки",9)
#print( dbase.getNagrAndType('3E18334CDD236883E268CE71B6CD2A884B13FE86A046015CCF39208CBA83C7D0','hod'))
#qwe.doSmth('1.2', '3E18334CDD236883E268CE71B6CD2A884B13FE86A046015CCF39208CBA83C7D0',db)

tz=timezone('Europe/Moscow')


print(bool(dbase.getLocalFood('хлеб')))