import re

class Node():
    
    def __init__(self,stroka,opisanie):
        self.nodes = []
        self.stroka = stroka
        self.opisanie = opisanie
    
    @staticmethod
    def connectDUO(node1,node2):
        node1.nodes.append(node2)
        node2.nodes.append(node1)
    
    def connectOneWay(node1,node2):
        node1.nodes.append(node2)
    
    def next(self,stroka):
        for x in self.nodes:                
            if (re.match(x.stroka,stroka) != None):        
                return x
        return 0
    
    def getDiscAvNodes(self):
        tmp = ""
        for x in self.nodes:
            if (tmp != ""):
                tmp = tmp + " или " + x.opisanie 
            else:
                tmp = tmp + x.opisanie
        return tmp

class FSM():

    def __init__(self):
        startNode = Node("начало","Скажите начало")
        diabet = Node("Д*д*иабет","Скажите диабет для подсчета")
        uroven = Node("\d+\.*,*\d*","Скажите уровень глюкозы")
        newProd = Node(".","Скажите продукт")
        grams = Node("\d+\.*,*\d*", "Скажите сколько грамм продукта") 
        calc = Node("подсчитать","Скажите подсчитать")
        
        self.cnode = startNode
        
        Node.connectDUO(startNode,diabet)
        
        Node.connectOneWay(diabet,uroven)
        Node.connectOneWay(uroven,startNode)
        
        Node.connectOneWay(uroven,newProd)
        Node.connectOneWay(newProd,startNode)
        
        Node.connectOneWay(newProd,grams)
        Node.connectOneWay(grams,calc)
        Node.connectOneWay(grams,startNode)
        Node.connectOneWay(grams,newProd)
        
        Node.connectOneWay(calc,startNode)
        
    def act(self,strAct):
        self.cnode = self.cnode.next(strAct)
        
    def getAvAct(self):
         return self.cnode.getDiscAvNodes()








    