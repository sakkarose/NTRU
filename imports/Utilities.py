import sys
import random

import numpy as npy
from math import gcd, log
from sympy import Poly, symbols, GF, invert

# Print full array without truncation
npy.set_printoptions(threshold=sys.maxsize)


# Check if a is a prime number
def primeCheck(a):
    if a <= 1:
        return False
    elif a == 2 or a == 3:
        return True
    else:
        for i in range(4, a // 2):
            if a % i == 0:
                return False
    return True


#
def padArray(a_in, a_out_size):
    return npy.pad(a_in, (a_out_size - len(a_in), 0), constant_values=0)


# Get the inverse of the polynomial (poly_in) in the Galois field, GF(poly_mod)
def polynomialInverse(poly_in, poly_I, poly_mod):
    x = symbols('x')
    Ppoly_I = Poly(poly_I, x)
    Npoly_I = len(Ppoly_I.all_coeffs())
    if primeCheck(poly_mod):
        try:
            inv = invert(Poly(poly_in, x).as_expr(), Ppoly_I.as_expr(), domain=GF(poly_mod, symmetric=False))
        except:
            return npy.array([])
    elif log(poly_mod, 2).is_integer():
        try:
            inv = invert(Poly(poly_in, x).as_expr(), Ppoly_I.as_expr(), domain=GF(2, symmetric=False))
            ex = int(log(poly_mod, 2))

            for a in range(1, ex):
                inv = ((2 * Poly(inv, x) - Poly(poly_in, x) * Poly(inv, x) ** 2) % Ppoly_I).trunc(poly_mod)
            inv = Poly(inv, domain=GF(poly_mod, symmetric=False))
        except:
            return npy.array([])
    else:
        return npy.array([])

    doubleCheck = npy.array(Poly((Poly(inv, x) * Poly(poly_in, x)) % Ppoly_I,
                                 domain=GF(poly_mod, symmetric=False)).all_coeffs(), dtype=int)
    if len(doubleCheck) > 1 or doubleCheck[0] != 1:
        sys.exit("Error : Error in polynomial inverse calculation !")

    return padArray(npy.array(Poly(inv, x).all_coeffs(), dtype=int), Npoly_I - 1)

#
