from permutations import *
from partitions import *

    
def test_gcoeff(n):
    for i in range(1,n+1):
        for par in Partition.all_strict(i):
            assert grothendieck_coeff(par.go_polynomial()) == par.go_coeff()

def generate_type1(n):
    for i in range(1,n+1):
        print("Partition: ["+str(i) +"]")
        print(Partition([i]).go_coeff())

def generate_type2(n):
    for i in range(1,n+1):
        print("Partition: ["+str(i)+", "+str(i-1) +"]")
        print(Partition([i,i-1]).go_coeff())
