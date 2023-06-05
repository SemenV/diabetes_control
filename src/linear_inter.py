import numpy as np



    
    
def get_linear_inter_val(tg,delimeter):
    xval = []
    yval = []
    for i in np.arange(0,5,delimeter):
        xval.append(i)
        yval_add = tg * i 
        yval.append(yval_add)
        
    return [xval, yval]
    
def get_linear_inter_point(tg,x):
    return tg*x
    
def get_linear_prepered(tg,delimeter):
    ret_val = []
    all_values = get_linear_inter_val(tg,delimeter)
    for i in range(len(all_values[0])-1):
        ret_val.append({"x": all_values[0][i], "y" : all_values[1][i]})
    return ret_val
    
    
#print(get_linear_inter_val(0.5773,0.5)  )
#print(get_linear_inter_point(0.5773,0.28865))
#print(get_linear_prepered(0.5773,0.5))