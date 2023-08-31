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


def test_equiv_class(n):
    for i in range(5,n+1):
        print([i,1])
        par = Partition([i,1])
        result_by_class =  par_by_equiv_re(par.go_coeff_inv_sorted())

        
        tail = []
        for i in range(5,i+1):
            tail.append(i)
        
        rep1 = [i+1,3,4,1,2] + tail
        rep2 = [i+1,2,3,1,4] + tail
        count1 = 0 
        count3 = 0 
        for cls in result_by_class:
            if cls[0][0].equiv_check(Permutation(rep1)):
                equiv_cls = Permutation(rep1).equiv_class()
                expect=[]
                for item in equiv_cls: 
                    if item.inverse().evaluate(3)<item.inverse().evaluate(4):
                        expect.append(item)
                assert len(expect) == len(cls),cls[0][0]
            if cls[0][0].equiv_check(Permutation(rep2)):
                assert len(cls) == len(Permutation(rep2).equiv_class()), cls[0][0]
            if len(cls) == 3:
                count3+=1
            if len(cls) == 1:
                count1+=1
        assert count3 ==1 and count1 == 2*i-5, count1


