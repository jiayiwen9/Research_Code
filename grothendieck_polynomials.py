import numpy
from permutations import *
import re

class Partition:
    def __init__(self,array) :
        self.length = len(array)
        self.array = array
        self.diagram = set()

        for i in range(self.length):
            for j in range(self.array[i]):
                self.diagram.add((i+1,i+1+j))
        
    def is_strict(self):
        for i in range(self.length-1):
            assert self.array[i]>self.array[i+1]

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

    return dict

#grothendieck_coeff(Partition([1]).go_polynomial())
#{ 2 1: 2,  3 1 2: 1}
