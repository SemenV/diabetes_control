import numpy as np


def calc_spl(A, B, proizv):

    
    promez = [A[0],A[1]]
    RB = []
    ur = []

    #первое уравнение
    eqInVert1 = []
    eqInVert1.append(A[0]**3)
    eqInVert1.append(A[0]**2)
    eqInVert1.append(A[0])
    eqInVert1.append(1)

    ur.append(eqInVert1)
    
    RB.append(B[0])
    
    #второе уранение
    eqInVert2 = []
    eqInVert2.append(A[1]**3)
    eqInVert2.append(A[1]**2)
    eqInVert2.append(A[1])
    eqInVert2.append(1)

    ur.append(eqInVert2)
    
    RB.append(B[1]) 

    #левая производная
    eqDerLeft = []
    eqDerLeft.append((A[0]**2)*3)
    eqDerLeft.append(A[0]*2)
    eqDerLeft.append(1)
    eqDerLeft.append(0)
    
    ur.append(eqDerLeft)
    
    RB.append(proizv[0])
    
    #правая производная
    eqDerRight = []
    eqDerRight.append((A[1]**2)*3)
    eqDerRight.append(A[1]*2)
    eqDerRight.append(1)
    eqDerRight.append(0)

    ur.append(eqDerRight)
    
    RB.append(proizv[1])
       
    #Возвращает ситему уранений которую надо решить и промежуток в котором строиться spline
    return [ur,RB,promez]

def print_arr(a):
    for s in a:
        print(*s)
        

def getSplines(A,B,proizv):
    k=0
    for i in range(len(A)-1):
        Anew = []
        Anew.append(A[k])
        Anew.append(A[k+1])

        Bnew = []
        Bnew.append(B[k])
        Bnew.append(B[k+1])

        newProizv = []
        newProizv.append(proizv[k])
        newProizv.append(proizv[k+1])
        k = k+1
        
        resh = calc_spl(Anew,Bnew,newProizv)
        matA = resh[0]
        matB = resh[1]
        print_arr(matA)
        print(matB)


        a = np.array([matA[0], matA[1],matA[2],matA[3]])

        b = np.array([matB[0], matB[1], matB[2], matB[3]])
        x = np.linalg.solve(a, b)

        print(x)
    
    
    
a = []
a.append(1)
a.append(3)
a.append(4)
a.append(6)


b = []
b.append(1)
b.append(3)
b.append(2)
b.append(3)


proizv = []
proizv.append(0)
proizv.append(0)
proizv.append(-1.6197)
proizv.append(0)


getSplines(a,b,proizv)