def get_all__main_spl_values_prepared(A,B):
    ret_val = []
    for i in range(len(A)):
        ret_val.append({"x": A[i], "y" : B[i]})
    print(ret_val)
    return ret_val
    
def get_all_main_spl_prepared_two(all_values):
    A = []
    B = []
    proizv = []
    i = 0
    while (i < len(all_values) - 1):
        A.append(all_values[i])
        B.append(all_values[i+1])
        proizv.append(all_values[i+2])
        i = i + 3

    return get_all__main_spl_values_prepared(A,B)
    
    
    
pr = [0.0, 0.0, 0.0, 1.0, 3.0, 0.0, 4.0, 2.0, -1.6197, 6.0, 3.0, 0.0]
print(get_all_main_spl_prepared_two(pr))