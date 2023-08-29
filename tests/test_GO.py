from permutations import *
from partitions import *

    
def test_gcoeff(n):
    for i in range(1,n+1):
        for par in Partition.all_strict(i):
            print(par)
            assert par.go_coeff_test() == par.go_coeff()

def test_gcoef(n):
    for i in range(1,n+1):
        print(i)
        assert Partition([i]).go_coeff_test() == Partition([i]).go_coeff()

def generate_type1(n):
    for i in range(1,n+1):
        print("Partition: ["+str(i) +"]")
        print(Partition([i]).go_coeff())

def generate_type2(n):
    for i in range(1,n+1):
        print("Partition: ["+str(i)+", "+str(i-1) +"]")
        print(Partition([i,i-1]).go_coeff())

def test_type1(n,start =3):
    for i in range(start,n+1):
        print(i)
        dict = Partition([i]).go_coeff_inv()
        for key in dict:
            assert key.size() == i+2 or key.size() ==i+1
            print(key)
            if key.size() == i+2 :
                assert dict[key] == 1
            else:
                if key.cab_check() and len(key.inc_subseq())>2:     
                    assert dict[key] == 1
                if len(key.inc_subseq()) == 2:
                    assert key.inc_subseq()[0][-1] == i+1
                    assert dict[key] == 2
                if key.cba_check() and len(key.inc_subseq())>2:      
                    assert dict[key] == 3


