import numpy as np

def get_linear_inter_val(tg,delimeter):
    xval = []
    yval = []
    for i in np.arange(0,5+delimeter,delimeter):

        xval.append(i)
        yval_add = tg * i 
        yval.append(yval_add)
        
    return [xval, yval]
    
def get_linear_inter_point(tg,x):
    return tg*x
    
def get_linear_prepered(tg,delimeter):
    ret_val = []
    all_values = get_linear_inter_val(tg,delimeter)
    for i in range(len(all_values[0])):
        ret_val.append({"x": all_values[0][i], "y" : all_values[1][i]})
    return ret_val
    
def get_main_linear_point(point):
    ret_val = []
    ret_val.append({"x": point[0], "y" : point[1]})
    return ret_val
    
