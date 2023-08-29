from partitions import *

for i in range(10):
    for par in Partition.all_strict(i):
        par.go_coeff_inv_sorted()