from permutations import *
import time


class Partition:
    memory = {}
    def __init__(self,array):
        self.length = len(array)
        self.array = array
        self.diagram = set()

        for i in range(self.length):
            for j in range(self.array[i]):
                self.diagram.add((i+1,i+1+j))
    def __repr__(self) -> str:
        if self.array != None:
            return str(self.array)
        else: 
            return str(self.diagram)
    
    def __eq__(self, __value: object) -> bool:
        return self.diagram == __value.diagram  
    
    def __hash__(self):
        return hash(str(self))

    def arr(self):
        return self.array

    def is_strict(self):
        for i in range(self.length-1):
            assert self.array[i]>self.array[i+1]

    def __len__(self):
        # number of rows 
        return self.length
    
    def size(self):
        # if self is partition of n, then return n 
        return len(self.diagram)
    
    def contain(self,other):
        # whether self contains other
        if self.size()< other.size() or len(self)<len(other) or self.size()==0:
            return False
        else:
            result = True
            for i in range(len(other)):
                temp = self.arr()[i]>other.arr()[i] or self.arr()[i] == other.arr()[i]
                result = result and temp
                return result
    # a method that returns the diagram
    def diag(self):
        d = self.diagram.copy()
        return d
    



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
        #self.is_strict()
        if len(self.diagram) == 0:
            return None
        if self in Partition.memory:
            return Partition.memory[self]
        if len(self.diagram) == 1:
            i,j = self.diagram.copy().pop()
            a= monomial_expansion_multiple_input([i])                 
            c= monomial_expansion_multiple_input([j])                 
            b = monomial_expansion_multiple_input([i,j])            
            result = combine_dict(a,c,b)
            Partition.memory[self] = result
            return Partition.memory[self]
 
        
        else:
            temp_arr = self.arr().copy()
            counter = 0
            for i in range(len(self)-1):
                if temp_arr[i]-1 > temp_arr[i+1]:
                    counter = i 
                    break
            counter = len(self)-1
            
            temp_arr[counter] -=1
            if temp_arr[counter] == 0:
                temp_par = Partition(temp_arr[:-1])
            else:
                temp_par = Partition(temp_arr)  
            

            result=temp_par.go_coeff()

            for (i,j) in self.diagram:
                if (i,j) not in temp_par.diagram:
                    part1 = mono_exp_multiple_input(i,result)
                    part2 = mono_exp_multiple_input(j,result)
                    part3 = mono_exp_multiple_input(j,part1)
                    result = combine_dict(part1,part2,part3)
            new_dict ={}
            for key,value in result.items():
                if value !=0:
                    new_dict[key] = value

            Partition.memory[self] = new_dict
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

    def go_coeff_sorted(self):
        return sorted(self.go_coeff().items(), key=lambda x: x[1])
    def go_coeff_inv_sorted(self):
        return sorted(self.go_coeff_inv().items(), key=lambda x: x[1])
'''
a= monomial_expansion_multiple_input([1])            
b = monomial_expansion_multiple_input([1,1])
result = combine_dict(a,a,b)
Partition.memory[Partition([1])] = result
'''


# count the number of terms in each coefficient.
def count_coeff(self):
    max_value = max(self.values())
    result = [0]*max_value
    for key in self:
        result[self[key]-1] +=1
    return result 
################

class Vertical_strip(Partition):

    def __init__(self, n = 0,shift =1 ):
        super(Vertical_strip,self).__init__([])
        self.array = None
        if n ==0:
            self.diagram = None
        else: 
            for i in range(1,n+1):
                self.diagram.add((shift,i))
            
    
    @classmethod
    def diagram_construct(cls,diagram = None):
        obj = cls()
        obj.array = None
        obj.diagram = diagram
        return obj
    
    def go_coeff(self):
        #self.is_strict()
        if len(self.diagram) == 0:
            return None
        if self in Partition.memory:
            return Partition.memory[self]
        if len(self.diagram) == 1:
            i,j = self.diagram.copy().pop()
            a= monomial_expansion_multiple_input([i])                 
            c= monomial_expansion_multiple_input([j])                 
            b = monomial_expansion_multiple_input([i,j])            
            result = combine_dict(a,c,b)
            
            new_dict ={}
            for key,value in result.items():
                if value !=0:
                    new_dict[key] = value
            Partition.memory[self] = new_dict
            return Partition.memory[self]
 
        
        else:
            temp_diagram = self.diagram.copy()
            temp_diagram.pop()
            temp_par = Vertical_strip.diagram_construct(temp_diagram)

            result=temp_par.go_coeff()

            for (i,j) in self.diagram:
                if (i,j) not in temp_par.diagram:
                    part1 = mono_exp_multiple_input(i,result)
                    part2 = mono_exp_multiple_input(j,result)
                    part3 = mono_exp_multiple_input(j,part1)
                    result = combine_dict(part1,part2,part3)
            new_dict ={key:value for key,value in result.items() if value!=0}
            Partition.memory[self] = new_dict
            return new_dict
    

class Square_shape(Partition):
    def __init__(self, n):
        array = []
        for i in reversed(range(1,n+1)):
            array.append(i)
        super().__init__(array)
    
    def go_coeff_sorted(self):
        list = sorted(self.go_coeff().items(), key=lambda x: x[1])
        new_list = []
        for pair in list: 
            item  = (pair[0].convert_to_partition(),pair[1])
            new_list.append(item)

        return new_list
'''
Partition([8]).go_coeff_inv()

{ 2 3 4 5 6 7 8 9 1: 2,  2 3 4 5 6 7 8 9 10 1: 1,  2 3 4 5 6 7 9 1 8: 2,  2 3 4 5 6 7 9 8 1: 3,  2 3 4 5 6 9 1 7 8: 2,  2 3 4 5 6 9 7 1 8: 3,  2 3 4 5 9 1 6 7 8: 2,  2 3 4 5 9 6 1 7 8: 3,  2 3 4 9 5 1 6 7 8: 3,  2 3 4 5 9 6 7 1 8: 1,  2 3 9 4 5 1 6 7 8: 1,  2 9 3 4 1 5 6 7 8: 1,  2 3 4 9 5 6 1 7 8: 1,  2 3 4 5 6 9 7 8 1: 1,  2 3 4 5 6 7 9 8 10 1: 1,  2 3 9 4 1 5 6 7 8: 3,  2 9 3 1 4 5 6 7 8: 3,  9 2 3 1 4 5 6 7 8: 1,  2 3 4 9 1 5 6 7 8: 2,  2 3 9 1 4 5 6 7 8: 2,  2 9 1 3 4 5 6 7 8: 2,  9 2 1 3 4 5 6 7 8: 3,  9 1 2 3 4 5 6 7 8: 2}

'''