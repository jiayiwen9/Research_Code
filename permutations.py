import numpy 

class Permutation:
    def __init__(self, array):
        # A dictionary is used to record the bijection
        self.map = {}
        self.array = array
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
    
    ## acting on the permutation by (i,i+1)
    def act(self,i):
        
        new_perm = self.array.copy()
        assert i < len(new_perm)
        if i< len(new_perm):
            temp = new_perm[i-1]
            new_perm.pop(i-1)
            new_perm.insert(i,temp)

            return Permutation(new_perm)


    #####################       Testing  Code #########################
    # from permutations import *
    # a=Permutation([4,2,3,1]) 
    # a.generate_word()
    