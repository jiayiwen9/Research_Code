import numpy 
from itertools import chain, combinations

class Permutation:
    def __init__(self, array):
        # A dictionary is used to record the bijection
        self.map = {}
        self.array = array
        self.range = len(array)
        if len(array) > 0:
            count = len(array)-1
            while count > -1:
                self.map[count+1] = array[count]
                count -= 1

    def __repr__(self) -> str:
            #print the oneline notation of the permutation
            oneline = ''
            for num in self.array:
                oneline += ' '+ str(num)
            return oneline
    
    def equal(self, other):
        if self.array == other.array:
            return True
        else: 
            return False
    
    # the image of a number under the permutation
    def evaluate(self, number):
    
        return self.map[number]
    
    def size(self):
        return max(self.map)

    
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

    # a function to compute P_k(v) 
    # i.e. the set of all permutations of the form 
    # w = v (a_1,k )(a_2, k ) ... (a_p,k) (k,b_1)... (k,b_q)
    # where a_p < ... < a_1 < b_q < ... < b_1
    # and l(w) = l(v) + p+q, and each transposition only increase the length by 1
    
    def p_set(self, k):
        result = []
        for subset in powerset(k,max(k+1,self.range+1)):
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

def powerset(k,max):
    # return all subsets of {1,2, ...,k-1,k+1,... , max}
    iterable = list(range(1,max+1))
    iterable.pop(k-1)
    temp=  list(chain.from_iterable(combinations(iterable, r) for r in range(len(iterable)+1)) )
    result = []
    for element in temp:
        result.append(sort(element,k))
    return result


def sort(set,k):
    result = list(reversed(set))
    for i in set: 
        if i >k:
            first_list = set[:set.index(i)]
            second_list = set[set.index(i):]
            result = list(reversed(first_list))
            result.extend(list(reversed(second_list)))
            break
    return result

#check whether a key in a dictionary or not ( when the type of the key is a permutation)
def check(self,dictionary):
    find = False
    key_0 = None
    for key in list(dictionary.keys()):
        if self.equal(key):
            find = True
            key_0 = key
            break
    
    return [find,key_0]

#edit a dictionary ( when the type of the key is a permutation)
def edit(key,value,dictionary):
    if check(key,dictionary)[0]:
        dictionary[check(key,dictionary)[1]] += value
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

#monomial_expansion([3,2,1]) expected { 2 3 4 1 :1}