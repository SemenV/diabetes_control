from DataBaseExec import *
from datetime import date, timedelta, datetime
import psycopg2


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
    )
    return connection
    
    
    
db = connect_db()
dbase = DataBaseExec(db)
dt = datetime.now()
print (dt)
print(dbase.connect_register_id_alice('LOL'))