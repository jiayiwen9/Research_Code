from partitions import *

for i in range(1,10):
    for par in Partition.all_strict(i):
        print(par.go_coeff_inv_sorted())