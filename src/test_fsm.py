

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




usr_fsm = FSM()
print(usr_fsm.actDB("начало","test_id_alice",db))
print(usr_fsm.actDB("диабет","test_id_alice",db))
print(usr_fsm.actDB("вафли","test_id_alice",db))
print(usr_fsm.actDB("1000","test_id_alice",db))
print(usr_fsm.actDB("абрикос","test_id_alice",db))
print(usr_fsm.actDB("100","test_id_alice",db))
print(usr_fsm.actDB("1.8","test_id_alice",db))
print(usr_fsm.actDB("посчитать","test_id_alice",db))
#print(usr_fsm.actDB("сохранить","test_id_alice",db))


def test_fsm_ok():
    assert usr_fsm.actDB("","test_id_alice",db) == [1, 'Скажите диабет для подсчета или Скажите настройки']
    assert usr_fsm.actDB("диабет","test_id_alice",db) == [2, 'Скажите начало или Скажите продукт']
    assert usr_fsm.actDB("вафли","test_id_alice",db) == [4, 'В продукте 62.5 углеводов Скажите начало или Скажите сколько грамм продукта']
    assert usr_fsm.actDB("20","test_id_alice",db) == [5, 'Скажите углеводный коэффициент или Скажите начало или Скажите продукт']
    assert usr_fsm.actDB("абрикос","test_id_alice",db) == [4, 'В продукте 9.0 углеводов Скажите начало или Скажите сколько грамм продукта']
    assert usr_fsm.actDB("30","test_id_alice",db) == [5, 'Скажите углеводный коэффициент или Скажите начало или Скажите продукт']
    assert usr_fsm.actDB("1.8","test_id_alice",db) == [6, 'Скажите начало или Скажите посчитать']
    assert usr_fsm.actDB("посчитать","test_id_alice",db) == [7, 'Вам рекомендовано сделать только на еду 2.74 едениц инсулина Скажите начало или Скажите сохранить или Скажите название нагрузки']
    assert usr_fsm.actDB("сохранить","test_id_alice",db) == [20, 'Результат сохранён Скажите начало']
    
    assert usr_fsm.actDB("начало","test_id_alice",db) == [1, 'Скажите диабет для подсчета или Скажите настройки']
    assert usr_fsm.actDB("диабет","test_id_alice",db) == [2, 'Скажите начало или Скажите продукт']
    assert usr_fsm.actDB("вафли","test_id_alice",db) == [4, 'В продукте 62.5 углеводов Скажите начало или Скажите сколько грамм продукта']
    assert usr_fsm.actDB("100","test_id_alice",db) == [5, 'Скажите углеводный коэффициент или Скажите начало или Скажите продукт']
    assert usr_fsm.actDB("абрикос","test_id_alice",db) ==  [4, 'В продукте 9.0 углеводов Скажите начало или Скажите сколько грамм продукта']
    assert usr_fsm.actDB("100","test_id_alice",db) ==  [5, 'Скажите углеводный коэффициент или Скажите начало или Скажите продукт']
    assert usr_fsm.actDB("1.8","test_id_alice",db) == [6, 'Скажите начало или Скажите посчитать']
    assert usr_fsm.actDB("посчитать","test_id_alice",db) == [7, 'Внимание: вы близки к порогу максимально количества углеводов в один приём пищи, проверьте корректность ввода или скорректируйте еду. Высокая доза инсулина 12.87 Скажите начало или Скажите сохранить или Скажите название нагрузки']
    
    
    assert usr_fsm.actDB("начало","test_id_alice",db) == [1, 'Скажите диабет для подсчета или Скажите настройки']
    assert usr_fsm.actDB("диабет","test_id_alice",db) == [2, 'Скажите начало или Скажите продукт']
    assert usr_fsm.actDB("вафли","test_id_alice",db) == [4, 'В продукте 62.5 углеводов Скажите начало или Скажите сколько грамм продукта']
    assert usr_fsm.actDB("1000","test_id_alice",db) == [5, 'Скажите углеводный коэффициент или Скажите начало или Скажите продукт']
    assert usr_fsm.actDB("абрикос","test_id_alice",db) ==  [4, 'В продукте 9.0 углеводов Скажите начало или Скажите сколько грамм продукта']
    assert usr_fsm.actDB("100","test_id_alice",db) ==  [5, 'Скажите углеводный коэффициент или Скажите начало или Скажите продукт']
    assert usr_fsm.actDB("1.8","test_id_alice",db) == [6, 'Скажите начало или Скажите посчитать']
    assert usr_fsm.actDB("посчитать","test_id_alice",db) == [6, 'Внимание: привышен порог максимального количества углеводов в один приём пищи, проверьте правильность ввода или скорректируйте продукты Скажите начало или Скажите посчитать']
    
    
    
    
    
    
    