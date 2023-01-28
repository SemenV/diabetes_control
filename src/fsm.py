import re
import requests
import json
import os

class Node():
    
    def __init__(self,stroka,opisanie,stage):
        self.nodesAllTime = []
        self.nextNodes = []
        self.stroka = stroka
        self.opisanie = opisanie
        self.stage = stage
        self.wrong = 0

    def doSmth(self,comm):
        pass
        

    @staticmethod
    def connectOneWayAllTime(node1,node2):
        node1.nodesAllTime.append(node2)
        
    @staticmethod
    def connectOneWayNextNode(node1,node2):
        node1.nextNodes.append(node2)
    
    def next(self,stroka):
        if (self.wrong == 0):
            for x in self.nodesAllTime:                
                if (re.match(x.stroka,stroka) != None):        
                    return [x,2]
            for x in self.nextNodes:                
                if (re.match(x.stroka,stroka) != None):        
                    return [x,2] 
        return [self,1] 
            
            

    def getDiscAvNodes(self):
        if (self.wrong == 0):
            tmp = ""
            for x in self.nodesAllTime:
                if (tmp != ""):
                    tmp = tmp + " или " + x.opisanie 
                else:
                    tmp = tmp + x.opisanie
            for x in self.nextNodes:
                if (tmp != ""):
                    tmp = tmp + " или " + x.opisanie 
                else:
                    tmp = tmp + x.opisanie
        else:
            print("==========")
            tmp = self.opisanie
            for x in self.nodesAllTime:
                if (tmp != ""):
                    tmp = tmp + " или " + x.opisanie 
                else:
                    tmp = tmp + x.opisanie
        return tmp





class Node2(Node):
    def doSmth(self,comm):
        z = {"eda" : {},"last" : {}}
        with open("ses.json", "w") as my_file:
            my_file.write(json.dumps(z))
        self.wrong = 0
    
class Node3(Node):
    def doSmth(self,comm):
        with open("ses.json", "r") as my_file:
            ses_json = json.loads(my_file.read())
            
        ses_json["uglS"] = comm

        with open("ses.json", "w") as my_file:
                my_file.write(json.dumps(ses_json))                
        self.wrong = 0


class Node4(Node):
    def doSmth(self,comm):
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
            self.wrong = 1
        else:
            self.wrong = 0
            with open("ses.json", "r") as my_file:
                ses_json = json.loads(my_file.read())
                
            ses_json["last"][comm] = ugl
            
            with open("ses.json", "w") as my_file:
                my_file.write(json.dumps(ses_json,ensure_ascii=False))
        
    def getDiscAvNodes(self):
        if (self.wrong == 0):
            tmp = ""
            for x in self.nodesAllTime:
                if (tmp != ""):
                    tmp = tmp + " или " + x.opisanie 
                else:
                    tmp = tmp + x.opisanie
            for x in self.nextNodes:
                if (tmp != ""):
                    tmp = tmp + " или " + x.opisanie 
                else:
                    tmp = tmp + x.opisanie
        else:
            tmp = "Продукт не найден " + self.opisanie
            for x in self.nodesAllTime:
                if (tmp != ""):
                    tmp = tmp + " или " + x.opisanie 
                else:
                    tmp = tmp + x.opisanie
        return tmp

class Node5(Node):
    def doSmth(self,comm):
        with open("ses.json", "r") as my_file:
                ses_json = json.loads(my_file.read())
        lastUgl = list(ses_json["last"].values())[0]
        lastProd = list(ses_json["last"].keys())[0]

        ses_json["eda"][lastProd] = [lastUgl,comm]
        ses_json["last"] = {}
        with open("ses.json", "w") as my_file:
            my_file.write(json.dumps(ses_json,ensure_ascii=False))
            
            
class Node6(Node):
    def doSmth(self,comm):
        pass
    
    


class FSM():

    def __init__(self):
        startNode = Node("Н*н*ачало|^$","Скажите начало",1)
        diabet = Node2("Д*д*иабет","Скажите диабет для подсчета",2)
        uroven = Node3("\d+\.*,*\d*","Скажите уровень глюкозы",3)
        newProd = Node4(".","Скажите продукт",4)
        grams = Node5("\d+\.*,*\d*", "Скажите сколько грамм продукта",5) 
        calc = Node("П*п*одсчитать","Скажите подсчитать",6)
        
        self.cnode = startNode
        
        Node.connectOneWayAllTime(startNode,diabet)
        Node.connectOneWayAllTime(diabet,startNode)
        
        Node.connectOneWayAllTime(diabet,uroven)
        Node.connectOneWayAllTime(uroven,startNode)
        
        Node.connectOneWayNextNode(uroven,newProd)
        Node.connectOneWayAllTime(newProd,startNode)
        
        Node.connectOneWayNextNode(newProd,grams)
        Node.connectOneWayNextNode(grams,calc)
        Node.connectOneWayAllTime(grams,startNode)
        Node.connectOneWayNextNode(grams,newProd)
        
        Node.connectOneWayAllTime(calc,startNode)
        
    def act(self,strAct):
        l = self.cnode.next(strAct)
        self.cnode = l[0]
        if (l[1] == 2):
            self.cnode.doSmth(strAct)
        return [l[1],self.cnode.stage] #равен 1 - команда не найдена
        
    def getAvAct(self):
         return self.cnode.getDiscAvNodes()
    
    def getStage(self):
        return self.cnode.stage







    