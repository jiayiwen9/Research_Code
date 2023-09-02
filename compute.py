from partitions import *


'''
#dynamic programming acceleration
# par is current partition to compute
current_result = {}

for i in range(par.arr()):
    temp = par.arr().copy
    if temp[i] ==1:
        temp = temp [:-1]
        if Partition(temp) in current_result:
            part1 = mono_exp_multiple_input(i+1,temp)
            part3 = mono_exp_multiple_input(i+1,part1)
            result = combine_dict(part1,part1,part3)
            new_dict ={}
            for key,value in result.items():
                if value !=0:
                    new_dict[key] = value
            current_result[par] = new_dict
            break
    else: 
        temp[i] -= 1
        if Partition(temp) in current_result:
            part1 = mono_exp_multiple_input(i+1,temp)
            part2 = mono_exp_multiple_input(temp[i]+1+i,temp)
            part3 = mono_exp_multiple_input(temp[i]+1+i,part1)
            result = combine_dict(part1,part2,part3)
            new_dict ={}
            for key,value in result.items():
                if value !=0:
                    new_dict[key] = value
            current_result[par] = new_dict
            break
'''

for i in range(2,6):
    print("--------------------------------------")
    print([i,1])
    a=Partition([i,1]).go_coeff_inv_sorted()
    for tup in a:
        print(tup)
    print("--------------------------------------")
        