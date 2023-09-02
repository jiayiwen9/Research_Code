import numpy
from permutations import *
import time


class Partition:
    def __init__(self,array):
        self.length = len(array)
        self.array = array
        self.diagram = set()

        for i in range(self.length):
            for j in range(self.array[i]):
                self.diagram.add((i+1,i+1+j))

    def __repr__(self) -> str:
        return str(self.array)
    
    def __eq__(self, __value: object) -> bool:
        return self.array == __value.array

    def arr(self):
        return self.array

    def is_strict(self):
        for i in range(self.length-1):
            assert self.array[i]>self.array[i+1]

    #generator function for all strict partitions of n
    @classmethod
    def all_strict(cls, n, max_part=None):
        if max_part is None:
            max_part = n

        if n == 0:
            yield Partition([])
        else:
            for i in range(1, 1 + min(max_part, n)):
                for p in cls.all_strict(n - i, i - 1):
                    parts = [i] + p.array
                    yield Partition(parts)
        
    def go_coeff(self):
        self.is_strict()
        
        if len(self.diagram) == 0:
            return None
        
        a= monomial_expansion([1])
        b = monomial_expansion([1,1])
        result = combine_dict(a,a,b)
        if len(self.diagram) == 1:
            return result
        if len(self.diagram) >1:
            for (i,j) in self.diagram:
                if i==1 and j==1:
                    continue
                else:
                    part1 = mono_exp_multiple_input(i,result)
                    part2 = mono_exp_multiple_input(j,result)
                    part3 = mono_exp_multiple_input(j,part1)
                    result = combine_dict(part1,part2,part3)
            new_dict ={}
            for key,value in result.items():
                if value !=0:
                    new_dict[key] = value
            return new_dict

    # return the coeff indexed by the inverse of permutation
    def go_coeff_inv(self):
        start_time = time.time()
        temp = self.go_coeff()
        result = {}
        for key in temp:
            result[key.inverse()]= temp[key]
        print("--- %s seconds ---" % (time.time() - start_time))
        return result    

    def go_coeff_inv_sorted(self):
        return sorted(self.go_coeff_inv().items(), key=lambda x: x[1])


# count the number of terms in each coefficient.
def count_coeff(self):
    max_value = max(self.values())
    result = [0]*max_value
    for key in self:
        result[self[key]-1] +=1
    return result 
################

'''
Partition([8]).go_coeff_inv()

{ 2 3 4 5 6 7 8 9 1: 2,  2 3 4 5 6 7 8 9 10 1: 1,  2 3 4 5 6 7 9 1 8: 2,  2 3 4 5 6 7 9 8 1: 3,  2 3 4 5 6 9 1 7 8: 2,  2 3 4 5 6 9 7 1 8: 3,  2 3 4 5 9 1 6 7 8: 2,  2 3 4 5 9 6 1 7 8: 3,  2 3 4 9 5 1 6 7 8: 3,  2 3 4 5 9 6 7 1 8: 1,  2 3 9 4 5 1 6 7 8: 1,  2 9 3 4 1 5 6 7 8: 1,  2 3 4 9 5 6 1 7 8: 1,  2 3 4 5 6 9 7 8 1: 1,  2 3 4 5 6 7 9 8 10 1: 1,  2 3 9 4 1 5 6 7 8: 3,  2 9 3 1 4 5 6 7 8: 3,  9 2 3 1 4 5 6 7 8: 1,  2 3 4 9 1 5 6 7 8: 2,  2 3 9 1 4 5 6 7 8: 2,  2 9 1 3 4 5 6 7 8: 2,  9 2 1 3 4 5 6 7 8: 3,  9 1 2 3 4 5 6 7 8: 2}

'''