from datetime import date, timedelta, datetime

class DataBaseExec:
    def __init__(self, db):
        self.__db = db
        self.__cur = db.cursor()
        
        
    def connect_register_id_alice(self,id_alice):
        sql = "INSERT INTO people (id_alice) VALUES ('" + id_alice + "');"
        self.__cur.execute(sql)
        self.__db.commit()
        
    def getIdByLogin(self, login, password):
        sql = "SELECT idd FROM people WHERE login = '" + login + "' AND passwordd = '" + password + "'"
        self.__cur.execute(sql)
        res = self.__cur.fetchall()
        return res
        
    #зачем ?    
    def getIdByAlice(self, id_alice):
        sql = "SELECT idd FROM people WHERE id_alice = '" + id_alice + "'"
        self.__cur.execute(sql)
        res = self.__cur.fetchall()
        return res
        
    def getDayMenu(self,userIdLogged,dt):
        dtStart = dt
        dtStart = dtStart.replace(hour=0, minute=0, second=0, microsecond=0)
        dtStartStr = dtStart.strftime('%Y-%m-%d %H:%M:%S')
        dtEnd = dt
        dtEnd = dtEnd.replace(hour=23, minute=59, second=59, microsecond=0)
        dtEndStr = dtEnd.strftime('%Y-%m-%d %H:%M:%S')
        sql = "SELECT ch_day, menu_eda,ch_nagruzka,time_nagruzka FROM eda WHERE useid = " + str(userIdLogged) + " AND ch_day > '" + dtStartStr + "+03' AND ch_day < '" + dtEndStr + "+03'"
        self.__cur.execute(sql)
        res = self.__cur.fetchall()
        return res
        
    def connect_login_psw_to_alice(self,login, password, userIdLogged ):
        sql = "UPDATE people SET login = '" + login + "', passwordd = '" + password + "' WHERE id_alice = '" + userIdLogged + "'"
        self.__cur.execute(sql)
        self.__db.commit()
        
        

        




    
        
    