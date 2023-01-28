from fsm import FSM

fsm = FSM()
print(fsm.getAvAct())
if (fsm.act("йцу")[0] == 1):
    print("Команда недоступна " + fsm.getAvAct())

fsm.act("диабет")
print(fsm.getAvAct())

if (fsm.act("йцу")[0] == 1):
    print("Команда недоступна " + fsm.getAvAct())

fsm.act("1")
print(fsm.getAvAct())

if (fsm.act("греча вареная")[0] == 1):
    print("Команда недоступна " + fsm.getAvAct())

print(fsm.getAvAct())




#fsm.act("qwe")
#print(fsm.getAvAct())
#fsm.act("хлеб")
#print(fsm.getAvAct())
#fsm.act("100")
#print(fsm.getAvAct())
#fsm.act("подсчитать")
#print(fsm.getAvAct())