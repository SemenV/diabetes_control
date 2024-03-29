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
     

def getSplines(A,B,proizv):
    k=0
    Xall = []
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

        a = np.array([matA[0], matA[1],matA[2],matA[3]])

        b = np.array([matB[0], matB[1], matB[2], matB[3]])
        x = np.linalg.solve(a, b)
        
        Xall.append(x)

        
        
    return Xall

def get_spline_point(A,B,proizv,point):
    Xall = getSplines(A,B,proizv)
    for k in range(len(A)-1):
            if ((point >= A[k]) and (point < A[k+1])):
                res = Xall[k][0] * point**3+ Xall[k][1]*point**2 + Xall[k][2]*point**1 + Xall[k][3]
                return res 
    return None

def get_spline_point_two(ABP,delimeter):
    A = []
    B = []
    proizv = []
    i = 0
    while (i < len(ABP) - 1):
        A.append(ABP[i])
        B.append(ABP[i+1])
        proizv.append(ABP[i+2])
        i = i + 3

    return get_spline_point(A,B ,proizv,delimeter)
    
def get_spl_val(A,B,proizv,delimeter):
    Xall = getSplines(A,B,proizv)
    xval = []
    yval = []
    for i in np.arange(0,A[len(A)-1]+delimeter,delimeter):

        xval.append(i)
        for k in range(len(A)-1):
            if ((i >= A[k]) and (i < A[k+1])):
                yval_add= Xall[k][0] * i**3+ Xall[k][1]*i**2 + Xall[k][2]*i**1 + Xall[k][3]
                yval.append(yval_add)
        if (i >= A[len(A)-1]):
            Ak = len(A)-2
            yval_add= Xall[Ak][0] * i**3+ Xall[Ak][1]*i**2 + Xall[Ak][2]*i**1 + Xall[Ak][3]   
            yval.append(yval_add)
    return [xval, yval]
    
def get_spl_prepered(A,B,proizv,delimeter):
    ret_val = []
    all_values = get_spl_val(A,B,proizv,delimeter)
    for i in range(len(all_values[0])):
        ret_val.append({"x": all_values[0][i], "y" : all_values[1][i]})
    return ret_val


def get_spl_prepered_two(ABP,delimeter):
    A = []
    B = []
    proizv = []
    i = 0
    while (i < len(ABP) - 1):
        A.append(ABP[i])
        B.append(ABP[i+1])
        proizv.append(ABP[i+2])
        i = i + 3

    return get_spl_prepered(A,B ,proizv,delimeter)
    
    
