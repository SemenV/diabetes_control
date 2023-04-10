from fsm import FSM
import pickle

fsm = FSM()

print(fsm.act(""))

print(fsm.act("диабет"))

print(fsm.act("1"))


print(fsm.act("сметана"))

print(fsm.act("1111"))

print(fsm.act("творог"))

print(fsm.act("222"))

with open('data.pickle', 'wb') as f:
    pickle.dump(fsm, f)
try:
    with open('йцу.pickle', 'rb') as f:
        res = data_new = pickle.load(f)
except:
    with open('data.pickle', 'wb') as f:
    pickle.dump(fsm, f)



print(res.act("1"))