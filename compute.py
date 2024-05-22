from partitions import *
"""
#par_max = []
par_square = []
par_strip = []
for i in range(1,5):
    par_strip.append([i])
    square = []
    p_max = []
    for j in reversed(range(1,i+1)):
        p_max.append(2*j-1)
        square.append(j)
    par_square.append(square)
#    par_max.append(p_max)


print("maximal shape:")
for par in par_max:
    print(par)
    list_res = Partition(par).go_coeff_inv_sorted()
    for item in list_res:
        print(item)
    print()
print()

print("square shape:")
for par in par_square:
    print(par)
    list_res = Partition(par).go_coeff_inv_sorted()
    for item in list_res:
        print(item)
    print()
print()
print("strip shape:")
for par in par_strip:
    print(par)
    list_res = Partition(par).go_coeff_inv_sorted()
    for item in list_res:
        print(item)
    print()
print()
"""
for j in range(2,6):
    for i in range(1,5):
        print("Vertical_strip=",i,"shifted by=",j)
        list= Vertical_strip(i,j).go_coeff_inv_sorted()
        for item in list:
            print(item)

        print()
