import re
import requests
import json
import os

class Node():
    
    def __init__(self,stroka,opisanie,stage):
        self.nodes = []
        self.stroka = stroka
        self.opisanie = opisanie
        self.stage = stage

    def doSmth(self,comm,usr_id):
        return [1,""]
    
    @staticmethod
    def connectOneWay(node1,node2):
        node1.nodes.append(node2)
        
        
    def next(self,stroka,usr_id):
        for x in self.nodes:                
            if (re.fullmatch(x.stroka,stroka) != None): 
                res = x.doSmth(stroka,usr_id)
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
    def doSmth(self,comm,usr_id):
        try:
            os.remove(usr_id + "ses.json")
        except:
            pass
        return [1, ""]     


     
class Node2(Node):
    def doSmth(self,comm,usr_id):
        z = {"eda" : {},"last" : {},"koef" : ""}
        with open(usr_id + "ses.json", "w",encoding='utf-8') as my_file:
            my_file.write(json.dumps(z))
        return [1, ""]
              
        
class Node4(Node):
    def doSmth(self,comm,usr_id):
        r = requests.get("https://ru-ru.openfoodfacts.org/category/" + comm + "/1.json")
        r_j = r.json()
        ugl = -1 
        i = 0;
        
        for i in range(r_j["page_count"]):
            try: r_j["products"][i]["nutriments"]["carbohydrates"]
            except:
                i = i + 1
                continue
            else:
                ugl = r_j["products"][i]["nutriments"]["carbohydrates"]
        if (ugl < 0):
            return [0, "Продукт не найден "]
        else:
            with open(usr_id + "ses.json", "r",encoding='utf-8') as my_file:
                ses_json = json.loads(my_file.read())
                
            ses_json["last"][comm] = ugl
            
            with open(usr_id + "ses.json", "w",encoding='utf-8') as my_file:
                my_file.write(json.dumps(ses_json,ensure_ascii=False))
            return [1, "В продукте " + str(ugl) + " углеводов "]

class Node5(Node):
    def doSmth(self,comm,usr_id):
        with open(usr_id + "ses.json", "r", encoding='utf-8') as my_file:
                ses_json = json.loads(my_file.read())
        lastUgl = list(ses_json["last"].values())[0]
        lastProd = list(ses_json["last"].keys())[0]

        ses_json["eda"][lastProd] = [lastUgl,comm]
        ses_json["last"] = {}
        with open(usr_id+"ses.json", "w",encoding='utf-8') as my_file:
            my_file.write(json.dumps(ses_json,ensure_ascii=False))
        return [1,""]
        
class Node6(Node):
    def doSmth(self,comm,usr_id):
        with open(usr_id+"ses.json", "r",encoding='utf-8') as my_file:
                ses_json = json.loads(my_file.read())
        ses_json["koef"] = comm
        with open(usr_id + "ses.json", "w",encoding='utf-8') as my_file:
            my_file.write(json.dumps(ses_json,ensure_ascii=False))
        return [1,""]
        
class Node6(Node):
    def doSmth(self,comm,usr_id):
        with open(usr_id+"ses.json", "r",encoding='utf-8') as my_file:
                ses_json = json.loads(my_file.read())
        ses_json["koef"] = comm
        with open(usr_id + "ses.json", "w",encoding='utf-8') as my_file:
            my_file.write(json.dumps(ses_json,ensure_ascii=False))
        return [1,""]
        
        
class Node7(Node):
    def doSmth(self,comm,usr_id):
        with open(usr_id+"ses.json", "r",encoding='utf-8') as my_file:
                ses_json = json.loads(my_file.read())
        counter = 0
        for key, val in ses_json["eda"].items():
            counter = counter + float(val[0])*float(val[1])/100 
        counter = counter * float(ses_json["koef"])
        counter = round(counter,2)
        ses_json["counter"] = counter
        with open(usr_id+"ses.json", "w",encoding='utf-8') as my_file:
            my_file.write(json.dumps(ses_json,ensure_ascii=False))
        return [1,"Вам рекомендовано сделать " + str(counter) + " едениц инсулина " ]
        
class FSM():

    def __init__(self):
        startNode = Node1("Н*н*ачало|^$","Скажите начало",1)
        diabet = Node2("Д*д*иабет","Скажите диабет для подсчета",2)
        newProd = Node4(".+","Скажите продукт",4)
        grams = Node5("\d+\.*,*\d*", "Скажите сколько грамм продукта",5) 
        uglK = Node6("\d+\.*,*\d*","Скажите углеводный коэффициент",6)
        calc = Node7("П*п*одсчитать|П*п*осчитать","Скажите подсчитать",6)
        
        self.cnode = startNode
        
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
    
    
    def act(self,comm,usr_id):
        l = self.cnode.next(comm,usr_id)
        self.cnode = l[0]
        return [l[1] + self.cnode.getDiscAvNodes(),self.cnode.stage]
        