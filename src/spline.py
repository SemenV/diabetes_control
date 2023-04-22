import numpy as np


def calc_spl(A, B, proizv):
    RB = []
    ur = []
    #2(n-1) уравнений и 4(n-1) значений в строке
    #формируем от 0 до длинны - 1
    #четность уранения отвечает за то сколько пар уранений было
    chetnUravn = -1
    for i in range(len(A)-1):
        chetnUravn = chetnUravn + 1;
        #в каждом узле кроме начального и конечного 2 уранения
        for j in range(2):
            currAd = i + j 
            fullArray = []
            #номер пары уравнений умножаем на 
            #a b c и d то есть 4 и получаем сколько 0 слева надо вставить
            for k in range(chetnUravn*4):
                fullArray.append(0)
            fullArray.append(A[currAd][0]**3)
            fullArray.append(A[currAd][0]**2)
            fullArray.append(A[currAd][0])
            fullArray.append(1)
            #кол-во всех уравнений 4(n-1) - заполненые
            for k in range((len(A) - 1)*4 - (chetnUravn*4 + 4)):
                fullArray.append(0)

            ur.append(fullArray)
            
            RB.append(B[currAd])
            
            
        
    
    if (len(ur) > 2):
        chetnUravn2 = -1
        for i in range(len(A)-1):
        chetnUravn2 = chetnUravn2 + 1;
            for j in range(2):
                currAd = i + j
                
    
    
    #4n уравнений
    first = [3* A[0][0], 2*A[0][0],1]
    for i in range((len(A) - 1)*4 -3):
        first.append(0)
    ur.append(first)
    
    
    last = []
    for i in range((len(A) - 1)*4 - 4):
        last.append(0)   
    last.append(3* A[len(A)-1][0]**2)
    last.append(2*A[len(A)-1][0])
    last.append(1)
    last.append(0)   
    
    
    ur.append(last)
        
        
        
    return [ur,RB]

def print_arr(a):
    for s in a:
        print(*s)
        


a = []
a.append([1])
a.append([3])
a.append([4])
a.append([6])


b = []
b.append([1])
b.append([3])
b.append([2])
b.append([3])


proizv = []
proizv.append([0])
proizv.append([0])
proizv.append([0])
proizv.append([0])




print_arr(calc_spl(a,b,proizv)[0])
print_arr(calc_spl(a,b,proizv)[1])

