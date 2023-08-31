import numpy 
from itertools import chain, combinations

class Permutation:
    def __init__(self, array=[1]):
        # A dictionary is used to record the bijection
        self.map = {}
        self.array = array
        if len(array) > 0:
            count = len(array)-1
            while count > -1:
                assert array[count] >0
                self.map[count+1] = array[count]
                count -= 1

    def inverse(self):
        array = list(range(1, self.size() + 1))
        for i in range(1, self.size() + 1):
            a = self.evaluate(i)
            array[a - 1] = i
        return Permutation(array)

    def __repr__(self) -> str:
            #print the oneline notation of the permutation
            oneline = ''
            for num in self.array:
                oneline += ' '+ str(num)
            return oneline
    
    def copy(self):
        return Permutation(self.array)

    def equal(self, other):
        return self.array == other.array

    def __eq__(self, other):
        return self.equal(other)
    
    def __hash__(self):
        return hash(str(self))
        
    # the image of a number under the permutation
    def evaluate(self, number):
    
        return self.map[number]
    
    def size(self):
        max_value =1
        for key in self.map:
            if self.evaluate(key) != key:
                max_value = max(max_value,key) 
        
        if max_value == 1:
            return 0 
        else:
            return max_value

    
    # inversions of the permutation
    def inversion(self):
        
        inv = 0
        count = len(self.map)
        while count > -1:
            for x in range(count):
                if self.map[x+1] > self.map[count]:
                    inv += 1
            count -= 1
        return inv
    
    ##### a method to generate all reduced word for a permutation
    #####################       Testing  Code #########################
    # from permutations import *
    # a=Permutation([4,2,3,1]) 
    # a.generate_word()
    ###################################################################
    def generate_word(self):
    
        word_list = []
        max = self.size()
        
        #help function
        def help_fn(perm, current):
            
            if perm.inversion() == 0:
                word_list.append(current)
                return
            else:
                for i in range(1,max):
                    new_current = current.copy()
                    if perm.act(i).inversion() == perm.inversion() -1:
                        new_current.append(i)
                        help_fn(perm.act(i),new_current)
                return
        


        if self.inversion() != 0:
            help_fn(self,[])
        return word_list
    
    ## acting on the permutation by (i,j)
    def act(self,i,j=None):
        if j == None:
            j= i+1
        new_perm = self.array.copy()
        
        if i==j:
            return self
        # make i < j 
        if i > j:
            temp = i
            i = j 
            j = temp 
        
        if j> len(new_perm):
            if i< len(new_perm) or i == len(new_perm):
                temp = new_perm[i-1]
                new_perm[i-1] = j
                for k in range(len(new_perm),j-1):
                    new_perm.insert(k,k)
                new_perm.insert(j-1,temp)
                return Permutation(new_perm)
            else:
                extra = list(range(len(new_perm)+1,j+1))
                new_perm.extend(extra)
                new_perm[i-1]= j
                new_perm[j-1] = i
                return Permutation(new_perm)
        else:
            assert i < len(new_perm)+1
            temp = new_perm[i-1]
            new_perm[i-1] = new_perm [j-1]
            new_perm[j-1]=temp

            return Permutation(new_perm)

    def act_sequence(self, array):
        temp = self.copy()
        for i in array:
            temp = temp.act(i)

        return temp
    # a function to compute P_k(v) 
    # i.e. the set of all permutations of the form 
    # w = v (a_1,k )(a_2, k ) ... (a_p,k) (k,b_1)... (k,b_q)
    # where a_p < ... < a_1 < b_q < ... < b_1
    # and l(w) = l(v) + p+q, and each transposition only increase the length by 1

    def p_set(self, k):
        result = []
        for subset in powerset(k,max(k+1,self.size()+1)):
            new_perm = self
            count =0
            find = True
            for i in subset: 
                inv = new_perm.inversion()
                new_perm = new_perm.act(i,k)
                if  new_perm.inversion() == inv +1:
                    if i < k:
                        count +=1
                    continue
                else: 
                    find = False
            if find == True:
                result.append([new_perm,count])    
        return result    
    
    def inc_subseq(self):
        result =[]
        if self.size() > 0:
            result.append([self.evaluate(1)])
            current = 0
            for i in range(2,self.size()+1):
                if self.evaluate(i) > self.evaluate(i-1):
                    result[current].append(self.evaluate(i))
                else:
                    current += 1
                    result.append([self.evaluate(i)])
        return result

    def equiv_class(self):
        result= []

        def help(self):
            if self in result:
                return
            result.append(self)
            max_range = self.size()-2
            for i in range(1,max_range+1):
                max_value = max(self.evaluate(i),self.evaluate(i+1),self.evaluate(i+2))
                min_value = min(self.evaluate(i),self.evaluate(i+1),self.evaluate(i+2))
                if self.evaluate(i) == min_value or self.evaluate(i+2) == max_value:
                    continue
                else: 
                    if min_value != self.evaluate(i+1) and self.act(i) not in result:
                        help(self.act(i))
                    if max_value != self.evaluate(i+1) and self.act(i+1) not in result:
                        help(self.act(i+1))
        
        help(self)
        return result
                            


    def equiv_check(self,other):
        return other in self.equiv_class()


def powerset(k,max):
    # return all subsets of {1,2, ...,k-1,k+1,... , max}
    iter1 = list(reversed(range(1,k)))
    iter1.extend(list(reversed(range(k+1,max+1))))
    result = list(chain.from_iterable(combinations(iter1,r) for r in range(len(iter1)+1)))
    return result 

def combine_dict(self,*other):
    result = self.copy()
    for dictionary in other:
        for key in dictionary:
            edit(key,dictionary[key],result)
    return result

def constant_mul(self,constant):
    for key in self:
        self[key] = constant * self[key]
    return self




def edit(key,value,dictionary):
    if key in dictionary:
        dictionary[key] += value
    else: 
        dictionary[key] = value
    return 
        

# expansion of a monomial as grothendieck basis
# input is an array representing the subscripts of the monomial
# output is a dictionary where the keys are Permutations and the value is the coefficient
def monomial_expansion(array,permutation = Permutation([1])):
    dict={}
    if len(array) == 0:
        return {permutation :1}
    def help_fn(array,current):
        
        if len(array) == 0:
            for key in current.keys():
                edit(key,current[key],dict)
            return
        else:
            k = array[0]
            for key in current.keys():
                value = current[key]
                new = {}
                for pair in key.p_set(k)[1:]:
                    #  negative coeff
                    if pair[1]% 2 == 1:
                        edit(pair[0],-value,new)
                    # positive coeff
                    if pair[1]% 2 ==0:
                        edit(pair[0],value,new)
                help_fn(array[1:],new)
            return

    if len(array) != 0:
        help_fn(array,{permutation:1})
    new_dict ={}
    for key,value in dict.items():
        if value !=0:
            new_dict[key] = value
   
    
    return new_dict

def mono_exp_multiple_input(index,poly = {Permutation([1]):1}):
    result ={}
    for key in poly:
        part1 = constant_mul(monomial_expansion([index],key),poly[key])
        result = combine_dict(result,part1)
    new_dict ={}
    for key,value in result.items():
        if value !=0:
            new_dict[key] = value
    return new_dict
    


def monomial_expansion_inv(array, permutation = Permutation([1])):
    temp = monomial_expansion(array,permutation.inverse())
    result = {}
    for key in temp:
        result[key.inverse()] = temp[key]
    return result

## this method is only for output and returns None
def par_by_equiv(array): 
    partition_result = []
    for item in array:
        if partition_result == []:
             partition_result.append([item])
        else:
            indicator = False
            for i in partition_result:
                if i[0][0].equiv_check(item[0]):
                    i.append(item)
                    indicator = True
                    break
            if indicator == False:
                partition_result.append([item])

    for i in partition_result:
        print(i)
# this is the same method but return an array instead
def par_by_equiv_re(array): 
    partition_result = []
    for item in array:
        if partition_result == []:
             partition_result.append([item])
        else:
            indicator = False
            for i in partition_result:
                if i[0][0].equiv_check(item[0]):
                    i.append(item)
                    indicator = True
                    break
            if indicator == False:
                partition_result.append([item])

    return partition_result
#monomial_expansion([3,2,1]) expected { 2 3 4 1 :1}
