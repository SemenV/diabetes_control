from datetime import date, timedelta, datetime
import psycopg2
from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2 import errors
from pytz import timezone

class DataBaseExec:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()
        
        
    def register_id_alice(self,id_alice):
        try:
            sql = "INSERT INTO people (id_alice,ch_role) VALUES ('" + id_alice + "' , 'user' );"
            self.__cur.execute(sql)
        except Exception as e:
            self.__db.rollback()
            print(e)
        else:
            self.__db.commit()
        
        try:
            sql = "INSERT INTO all_nagruzka (useid, nagruzka_name,nagruzka,nagr_type) VALUES ( (SELECT idd FROM people WHERE id_alice = '" + id_alice + "'), 'beg','[0.0, 0.0, 11.43, 2.0, 2.0, 11.43]','subspline')" 
            self.__cur.execute(sql)
        except Exception as e:
            self.__db.rollback()
            print(e)
        else:
            self.__db.commit()
        
        

        try:
            sql = "INSERT INTO all_nagruzka (useid, nagruzka_name,nagruzka,nagr_type) VALUES ( (SELECT idd FROM people WHERE id_alice = '" + id_alice + "'), 'hod','1.619','linear')" 
            self.__cur.execute(sql)
        except Exception as e:
            self.__db.rollback()
            print(e)
        else:
            self.__db.commit()
        
    def getIdByLoginPsw(self, login, password):
        sql = "SELECT idd FROM people WHERE login = '" + login + "' AND passwordd = '" + password + "'"
        self.__cur.execute(sql)
        res = self.__cur.fetchall()
        return res
        
       
    def getNagruzkaNames(self, useid):
        sql = "SELECT nagruzka_name FROM all_nagruzka WHERE useid = '" + useid + "'"
        self.__cur.execute(sql)
        res = self.__cur.fetchall()
        return res
    
    
    def getNagruzkaPoints(self, useid,name):
        sql = "SELECT nagruzka FROM all_nagruzka WHERE useid = '" + useid + "' and nagruzka_name = '" + name +"'"
        self.__cur.execute(sql)
        res = self.__cur.fetchall()
        return res
    

        
    def setNagruzka(self, useid, nagruzka_name, nagruzka,nagr_type):
        sql = "DO $$ BEGIN UPDATE all_nagruzka SET nagruzka = '" +nagruzka+ "', nagr_type = '" +nagr_type+ "' WHERE useid = "+ useid +" and nagruzka_name = '" +nagruzka_name+ "'; IF NOT FOUND THEN INSERT INTO all_nagruzka (useid, nagruzka_name, nagruzka, nagr_type) VALUES (" +useid +", '" + nagruzka_name +"' , '"+ nagruzka +"','"+ nagr_type +"'); END IF; END; $$"
        self.__cur.execute(sql)
        self.__db.commit()
        
    
    def getIdByAlice(self, id_alice):
        sql = "SELECT idd FROM people WHERE id_alice = '" + id_alice + "'"
        self.__cur.execute(sql)
        res = self.__cur.fetchall()
        return res
        
    def getDayMenu(self,userIdLogged,dt):
        dtStart = dt
        dtStart = dtStart.replace(hour=0, minute=0, second=0, microsecond=0)
        dtStartStr = dtStart.strftime('%Y-%m-%d %H:%M:%S+03')
        dtEnd = dt
        dtEnd = dtEnd.replace(hour=23, minute=59, second=59, microsecond=0)
        dtEndStr = dtEnd.strftime('%Y-%m-%d %H:%M:%S+03')
        sql = "SELECT ch_day, menu_eda FROM eda WHERE useid = " + str(userIdLogged) + " AND ch_day > '" + dtStartStr + "' AND ch_day < '" + dtEndStr + "'"
        self.__cur.execute(sql)
        res = self.__cur.fetchall()
        return res
        
    def setMenuRow(self,id_alice,eda):
        tz=timezone('Europe/Moscow')
        dt = datetime.now(tz).strftime('%Y-%m-%d %H:%M:%S')
        id_user = str(self.getIdByAlice(id_alice)[0][0])
        sql = "INSERT INTO eda (useid, ch_day,menu_eda) VALUES ('" + id_user + "','" + dt  + "','"+ eda + "');"
        self.__cur.execute(sql)
        self.__db.commit()
    
    def delTmpReg(self,id_alice):
        try: 
            sql = "DELETE FROM reg_tmp WHERE id_alice = '" + id_alice + "';"
            self.__cur.execute(sql)
        except Exception as e:
            self.__db.rollback()
            print(e)
        else:
            self.__db.commit()
    

    def insertTmpRegIdAlice(self,id_alice):
        sql = "INSERT INTO reg_tmp (id_alice) VALUES ('" + id_alice + "');"
        self.__cur.execute(sql)
        self.__db.commit()
    
    
    def check_login(self,login):
        sql = "SELECT 1 FROM people WHERE login = '" + login + "'"
        self.__cur.execute(sql)
        res = self.__cur.fetchall()
        return res
        
      
    def setTmpLogin(self,id_alice, login):
        sql = "UPDATE reg_tmp SET login = '" + login + "' WHERE id_alice = '" + id_alice + "'"
        self.__cur.execute(sql)
        self.__db.commit()
    
    def getTmpLogin(self,id_alice):
        sql = "SELECT login FROM reg_tmp WHERE id_alice = '" + id_alice + "'"
        self.__cur.execute(sql)
        res = self.__cur.fetchall()
        return res
        
        
    def setTmpPsd(self,id_alice, passwordd):
        sql = "UPDATE reg_tmp SET passwordd = '" + passwordd + "' WHERE id_alice = '" + id_alice + "'"
        self.__cur.execute(sql)
        self.__db.commit()
        
        
    def connect_login_psw_to_alice(self,login, password, id_alice ):
        sql = "UPDATE people SET login = '" + login + "', passwordd = '" + password + "' WHERE id_alice = '" + id_alice + "'"
        self.__cur.execute(sql)
        self.__db.commit()
        
    def getTmpFood(self, id_alice):
        sql = "SELECT current_food FROM eda_tmp WHERE id_alice = '" + id_alice + "'"
        self.__cur.execute(sql)
        res = self.__cur.fetchall()
        return res
        
    def setTmpFood(self,id_alice,current_food):
        sql = "INSERT INTO eda_tmp (id_alice,current_food) VALUES ('" + id_alice + "' , '" + current_food + "');"
        self.__cur.execute(sql)
        self.__db.commit()
        
    def deleteFromTmpTbale(self,id_alice):
        try: 
            sql = "DELETE FROM eda_tmp WHERE id_alice = '" + id_alice + "';"
            self.__cur.execute(sql)
        except Exception as e:
            self.__db.rollback()
            print(e)
        else:
            self.__db.commit()
    
        
    def updateTmpFood(self,id_alice,current_food):
        sql = "UPDATE eda_tmp SET current_food = '" + current_food + "' WHERE id_alice = '" + id_alice + "'"
        self.__cur.execute(sql)
        self.__db.commit()


    def getStageDB(self,id_alice):
        sql = "SELECT COALESCE((SELECT  stage FROM people WHERE id_alice = '" + id_alice+ "'), 1);"
        self.__cur.execute(sql)
        res = self.__cur.fetchall()
        return res
        
    def updateStage(self,id_alice,stage):
        sql = "UPDATE people SET stage = '" + str(stage) + "' WHERE id_alice = '" + id_alice + "'"
        self.__cur.execute(sql)
        self.__db.commit()
        
        
    def getNagrAndType(self,id_alice,nagrName):
        id_user = str(self.getIdByAlice(id_alice)[0][0])
        sql = "SELECT nagruzka, nagr_type FROM all_nagruzka where nagruzka_name = '" + nagrName + "' and useid = '" + id_user + "';"
        self.__cur.execute(sql)
        res = self.__cur.fetchall()
        return res 
        
    def getNagrAndTypeById(self,useid,nagrName):
        sql = "SELECT nagruzka, nagr_type FROM all_nagruzka where nagruzka_name = '" + nagrName + "' and useid = '" + str(useid) + "';"
        self.__cur.execute(sql)
        res = self.__cur.fetchall()
        return res 
    
    
    def getLocalFood(self,prod_name):
        sql = "SELECT  prod_param FROM localfood WHERE prod_name = '" + prod_name+ "';"
        self.__cur.execute(sql)
        res = self.__cur.fetchall()
        return res
    
    def romoveFromLocalFood(self,prod_name):
        try: 
            sql = "DELETE FROM localfood WHERE prod_name = '" + prod_name + "';"
            self.__cur.execute(sql)
        except Exception as e:
            self.__db.rollback()
            print(e)
        else:
            self.__db.commit()
        
    def getAllLocalFood(self):
        sql = "SELECT prod_name, prod_param	FROM localfood;"
        self.__cur.execute(sql)
        res = self.__cur.fetchall()
        return res
        
    
    def getUserRole(self, useid):
        sql = "SELECT ch_role FROM people where idd = " + str(useid) + ";"
        self.__cur.execute(sql)
        res = self.__cur.fetchall()
        return res
        
        
    def setFoodLocalFood(self, prod_name, prod_param):
        sql = "DO $$ BEGIN UPDATE localfood SET prod_name = '" +prod_name+ "', prod_param = '" + str(prod_param)+ "' WHERE prod_name = '"+ prod_name + "'; IF NOT FOUND THEN INSERT INTO localfood (prod_name, prod_param) VALUES ('" +prod_name +"', " + str(prod_param) + "); END IF; END; $$"
        self.__cur.execute(sql)
        self.__db.commit()
        