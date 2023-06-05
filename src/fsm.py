import re
import json
import os
from DataBaseExec import *
import psycopg2
from psycopg2.errorcodes import UNIQUE_VIOLATION
from psycopg2 import errors
import requests 
import sys




class Node():
    
    def __init__(self,stroka,opisanie,stage):
        self.nodes = []
        self.stroka = stroka
        self.opisanie = opisanie
        self.stage = stage
    
    def getStage(self):
        return self.stage


    def doSmth(self,comm,usr_id,db):
        return [1,""]
    
    @staticmethod
    def connectOneWay(node1,node2):
        node1.nodes.append(node2)
        
        
    def next(self,stroka,usr_id,db):
        for x in self.nodes:                
            if (re.fullmatch(x.stroka,stroka) != None): 
                res = x.doSmth(stroka,usr_id,db)
                if (res[0] == 0):
                    return [self,res[1]]
                else:
                    return [x,res[1]]
        if (self.stage != 1):
            return [self,"Команда не найдена "]
        else:
            return [self,""]
    
    def getDiscAvNodes(self):
        tmp = ""
        for x in self.nodes:
            if (tmp != ""):
                tmp = tmp + " или " + x.opisanie 
            else:
                tmp = tmp + x.opisanie
        return tmp


#============================================================================================
class Node1(Node):
    def doSmth(self,comm,usr_id,db):
        dbase = DataBaseExec(db)
        dbase.register_id_alice(usr_id)
        try: 
            os.remove(usr_id + "ses.json")
        except:
            pass
        return [1, ""]     


     
class Node2(Node):
    def doSmth(self,comm,usr_id,db):
        dbase = DataBaseExec(db)
        dbase.deleteFromTmpTbale(usr_id)
        z = {"eda" : {},"last" : {},"koef" : "", "nagruzka" : {}}
        dbase.setTmpFood(usr_id,json.dumps(z))
        return [1, ""]
        
              
        
class Node4(Node):
    def doSmth(self,comm,usr_id,db):
        r = requests.get("https://ru-ru.openfoodfacts.org/category/" + comm + "/1.json")
        r_j = r.json()
        ugl = -1 
        i = 0;
        rangeAmount = 0
        if (r_j["page_count"] > 5):
            rangeAmount = 5
        else:
            rangeAmount = r_j["page_count"]
        
        for i in range(rangeAmount):
            try: r_j["products"][i]["nutriments"]["carbohydrates"]
            except:
                i = i + 1
                continue
            else:
                ugl = float(r_j["products"][i]["nutriments"]["carbohydrates"])
        if (ugl < 0):
            return [0, "Продукт не найден "]
        else:
            dbase = DataBaseExec(db)
            ses_json = json.loads(dbase.getTmpFood(usr_id)[0][0])
            ses_json["last"][comm] = ugl

            dbase.updateTmpFood(usr_id,json.dumps(ses_json, ensure_ascii=False ))
            return [1, "В продукте " + str(ugl) + " углеводов "]
            

class Node5(Node):
    def doSmth(self,comm,usr_id,db):
        dbase = DataBaseExec(db)
        ses_json = json.loads(dbase.getTmpFood(usr_id)[0][0])
    
        lastUgl = list(ses_json["last"].values())[0]
        lastProd = list(ses_json["last"].keys())[0]

        ses_json["eda"][lastProd] = [lastUgl,comm]
        ses_json["last"] = {}
        
        dbase.updateTmpFood(usr_id,json.dumps(ses_json, ensure_ascii=False ))
        return [1,""]
        
class Node6(Node):
    def doSmth(self,comm,usr_id,db):
        dbase = DataBaseExec(db)
        ses_json = json.loads(dbase.getTmpFood(usr_id)[0][0])

        ses_json["koef"] = comm
        dbase.updateTmpFood(usr_id,json.dumps(ses_json, ensure_ascii=False ))

        return [1,""]
        
        
        
class Node7(Node):
    def doSmth(self,comm,usr_id,db):
        saveEda(comm,usr_id,db)

        
    def saveEda(self,comm,usr_id,db):
        dbase = DataBaseExec(db)
        ses_json = json.loads(dbase.getTmpFood(usr_id)[0][0])

        counter = 0
        for key, val in ses_json["eda"].items():
            counter = counter + float(val[0])*float(val[1])/100      
        counter = counter / 10
        counter = counter * float(ses_json["koef"])
        counter = round(counter,2)
        ses_json["counter"] = counter
        
        dbase.updateTmpFood(usr_id,json.dumps(ses_json, ensure_ascii=False ))

        return [1,"Вам рекомендовано сделать " + str(counter) + " едениц инсулина " ]
        
        
        
        
        
class Node100(Node):
    def doSmth(self,comm,usr_id,db):
        return [1,""]
        
class Node101(Node):
    def doSmth(self,comm,usr_id,db):
        dbase = DataBaseExec(db)
        dbase.delTmpReg(usr_id)
        dbase.insertTmpRegIdAlice(usr_id)
        return [1,""]  

class Node102(Node):
    def doSmth(self,comm,usr_id,db):
        dbase = DataBaseExec(db)
        if (bool(dbase.check_login(usr_id))):
            return [0,"Уже есть такой пользователь"]
        else: 
            dbase.setTmpLogin(usr_id, comm)
            return [1,""]  


class Node103(Node):
    def doSmth(self,comm,usr_id,db):
        dbase = DataBaseExec(db)
        tmpLogin = dbase.getTmpLogin(usr_id)[0][0]
        dbase.connect_login_psw_to_alice(tmpLogin, comm, usr_id)
        return [1,"Ваш логин и пароль были обновлены."]             


        
class FSM():
    allStages = {}
    
    def addStage(self,n): 
        staage = n.getStage()
        self.allStages[staage] = n
        return n
    
    
    def getNodeByStage(self,stage):
        return self.allStages[stage]    
    

    def __init__(self):
        startNode = self.addStage(Node1("Н*н*ачало|^$","Скажите начало",1))
        diabet = self.addStage(Node2("Д*д*иабет","Скажите диабет для подсчета",2))
        newProd = self.addStage(Node4(".+","Скажите продукт",4))
        grams = self.addStage(Node5("\d+\.*,*\d*", "Скажите сколько грамм продукта",5))
        uglK = self.addStage(Node6("\d+\.*,*\d*","Скажите углеводный коэффициент",6))
        calc = self.addStage(Node7("П*п*одсчитать|П*п*осчитать","Скажите подсчитать",7))
        
        setings = self.addStage(Node100("Н*н*астройки|Н*н*астроить","Скажите настройки",100))
        register = self.addStage(Node101("Р*р*егистрация","Скажите регистрация",101))
        say_login = self.addStage(Node102("\w*","Скажите логин",102))
        say_psd = self.addStage(Node103("\w*","Скажите Пароль",103))
             
        
        Node.connectOneWay(startNode,diabet)
        Node.connectOneWay(diabet,startNode)
        
        
        Node.connectOneWay(diabet,newProd)
        Node.connectOneWay(newProd,startNode)
        
        Node.connectOneWay(newProd,grams)
        Node.connectOneWay(grams,uglK)
        Node.connectOneWay(grams,startNode)
        Node.connectOneWay(grams,newProd)
        
        Node.connectOneWay(uglK,startNode)
        
        Node.connectOneWay(uglK,calc)
        Node.connectOneWay(calc,startNode)
    
    
    
    
        Node.connectOneWay(startNode,setings)
        Node.connectOneWay(setings,startNode)
        
        Node.connectOneWay(setings,register)
        Node.connectOneWay(register,startNode)
        
        Node.connectOneWay(register,say_login)
        Node.connectOneWay(say_login,startNode)
        
        Node.connectOneWay(say_login,say_psd)
        Node.connectOneWay(say_psd,startNode)
    
    
    
    
    
    def act(self,comm,usr_id,db,stage):
        cNode = self.getNodeByStage(stage)
        if (cNode.getStage() == 1):
            cNode.doSmth(comm,usr_id,db)
        l = self.getNodeByStage(stage).next(comm,usr_id,db)
        return [l[0],l[1] + l[0].getDiscAvNodes()]
    
    def actDB(self,comm,usr_id,db):
        dbase = DataBaseExec(db)
        stage = dbase.getStageDB(usr_id)[0][0]

        l = self.act(comm,usr_id,db,stage)
        newStage = l[0].getStage()
        dbase.updateStage(usr_id,newStage)
        return [l[0].getStage(),l[1]]
        
        