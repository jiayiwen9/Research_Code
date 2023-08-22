import numpy
from permutations import *
import re
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

    def go_polynomial(self): 
        self.is_strict()
        # compute the GO polynomial for a strict partition
        if len(self.diagram) == 0:
            return None
        if len(self.diagram) == 1:
            return {'x_1':2,'x_1x_1':1}
        if len(self.diagram) > 1:
            poly1 = {'x_1':2,'x_1x_1':1}
            for (i,j) in self.diagram:
                if i == 1 and j ==1:
                    continue
                else:
                    if i != j:
                        poly2 = {'x_'+str(i):1, 'x_'+str(j):1, 'x_'+str(i)+'x_'+str(j):1}
                    else: 
                        poly2 = {'x_'+str(i):2,'x_'+str(i)+'x_'+str(i):1}
                    poly1 = polynomial_coefficients(poly1,poly2)

            return(poly1)
        
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
                temp = result.copy()
                if i==1 and j==1:
                    continue
                else:
                    result = {}
                    for key in temp.keys():
                        part1 = constant_mul(monomial_expansion([i],key),temp[key])
                        part2 = constant_mul(monomial_expansion([j],key),temp[key])
                        part3 = constant_mul(monomial_expansion([i,j],key),temp[key])
                        result = combine_dict(result,part1,part2,part3)
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


def polynomial_coefficients(poly1,poly2):
    """
    Computes the coefficients of each monomial in the product of the given polynomials.

    Returns:
    dictionary of coefficients of each monomial in the product of the given polynomials, with variable names as keys and exponents as values
    """
    # Initialize the two polynomials as dictionaries of coefficients
    #poly1 = {'x1': 1, 'x2': 1, 'x1x2': 1}  # represents x1 + x2 + x1*x2
    #poly2 = {'x2': 1, 'x3': 1, 'x2x3': 1}  # represents x2 + x3 + x2*x3

    # Initialize an empty dictionary to store the coefficients of each monomial
    coefficients = {}

    # Loop through each term in the first polynomial
    for var1, exp1 in poly1.items():
        # Loop through each term in the second polynomial
        for var2, exp2 in poly2.items():
            # Multiply the coefficients of the two terms to get the coefficient of the monomial
            coefficient = poly1.get(var1) * poly2.get(var2)
            # Add the coefficient to the dictionary of coefficients
            # at the appropriate key (variable names with concatenated exponents)
            key = var1 + var2
            if key in coefficients:
                coefficients[key] += coefficient
            else:
                coefficients[key] = coefficient

    return coefficients


def convert(var):
    assert "x" in var
    str_list = re.split("x_",var)
    return [int(i) for i in str_list[1:]]

# compute the grothendieck basis coefficients of a polynomial
def grothendieck_coeff(polynomial):
    dict = {}

    for var , coeff in list(polynomial.items()):
        array = convert(var)
        current = monomial_expansion(array)
        for key in current.keys():
            edit(key,current[key]*coeff,dict)
    new_dict ={}
    for key,value in dict.items():
        if value !=0:
            new_dict[key] = value
   
    
    return new_dict 

Partition([2]).go_coeff()

################
#grothendieck_coeff(Partition([1]).go_polynomial())
#{ 2 1: 2,  3 1 2: 1}


'''
Partition([8]).go_coeff_inv()

{ 2 3 4 5 6 7 8 9 1: 2,  2 3 4 5 6 7 8 9 10 1: 1,  2 3 4 5 6 7 9 1 8: 2,  2 3 4 5 6 7 9 8 1: 3,  2 3 4 5 6 9 1 7 8: 2,  2 3 4 5 6 9 7 1 8: 3,  2 3 4 5 9 1 6 7 8: 2,  2 3 4 5 9 6 1 7 8: 3,  2 3 4 9 5 1 6 7 8: 3,  2 3 4 5 9 6 7 1 8: 1,  2 3 9 4 5 1 6 7 8: 1,  2 9 3 4 1 5 6 7 8: 1,  2 3 4 9 5 6 1 7 8: 1,  2 3 4 5 6 9 7 8 1: 1,  2 3 4 5 6 7 9 8 10 1: 1,  2 3 9 4 1 5 6 7 8: 3,  2 9 3 1 4 5 6 7 8: 3,  9 2 3 1 4 5 6 7 8: 1,  2 3 4 9 1 5 6 7 8: 2,  2 3 9 1 4 5 6 7 8: 2,  2 9 1 3 4 5 6 7 8: 2,  9 2 1 3 4 5 6 7 8: 3,  9 1 2 3 4 5 6 7 8: 2}

'''