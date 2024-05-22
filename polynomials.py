from partitions import * 
from collections import UserDict

class Polynomial(UserDict):
    def remove_zero(self):
        new_dict = self.copy()
        for key,value in self.items():
            if value == 0:
                new_dict.pop(key)
        return Polynomial(new_dict)
    
    @classmethod
    def add_poly(cls, *args):
        new_dict = combine_dict(*args)
        return new_dict.remove_zero()
    
    def mul_poly(self, *args):
        new_dict = self.copy()
        for dict in args:
            temp = {}
            for key_1,value_1 in dict.items():
                for key_2,value_2 in new_dict.items():
                    temp[[x+y for x,y in zip(key_1,key_2)]] = value_1 * value_2
                    # to complete

        return new_dict.remove_zero()


    @classmethod
    def orthogonal_groth_poly(cls, partition):
        poly = Polynomial()
        for tup in partition.diag():
            assert len(tup) == 2
            i, j = tup
            mono_1 = []
            mono_2 = []

            mono_1[i-1] =1 
            mono_2[j-1] =1
            poly = Polynomial.add_poly( Polynomial({mono_1:1}), Polynomial({mono_2:1}), Polynomial.mul_poly( Polynomial({mono_1:1}), Polynomial({mono_2:1})))
            return poly


