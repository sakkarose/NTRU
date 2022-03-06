import sys
import random
import numpy as npy
from math import log
from sympy import Poly, symbols, GF, invert

# Print full array without truncation
npy.set_printoptions(threshold=sys.maxsize)


# Check if num is a prime number
def primeCheck(num):
    if num <= 1:
        return False
    elif num == 2 or num == 3:
        return True
    else:
        for i in range(4, num // 2):
            if num % i == 0:
                return False
    return True


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


# Pad a numpy integer to a numpy array with leading zeros.
def padArray(a_in, a_out_size):
    return npy.pad(a_in, (a_out_size - len(a_in), 0), constant_values=0)


# Generate a numpy array for f, p and r. L is length, P for 1 and M for -1, the remaining is 0
def generateRandom1n0(L, P, M):
    # Making sure the length is legit
    if P + M > L:
        sys.exit("ERROR : Do the input again, P + M must be larger than L.")

    # Generate empty array of 0's
    r = npy.zeros((L,), dtype=int)

    # Put 1 and -1 in array (not random yet)
    for i in range(L):
        if i < P:
            r[i] = 1
        elif i < P + M:
            r[i] = -1
        else:
            break

    # Randomise the r array
    npy.random.shuffle(r)
    return r


# Numpy array to string array
def array2String(array):
    string = npy.array_str(array)
    string = string.replace("[", "", 1)
    string = string.replace("]", "", 1)
    string = string.replace("\n", "")
    string = string.replace("     ", " ")
    string = string.replace("    ", " ")
    string = string.replace("   ", " ")
    string = string.replace("  ", " ")
    return string


# String to binary of string, each bit is an integer of numpy array earlier
def string2Bit(string):
    return npy.array(list(bin(int.from_bytes(str(string).encode(), "big")))[2:], dtype=int)


# Reverse string2Bit
def bit2String(bit):
    # Check number of bits is divisible by 8
    a = padArray(bit, len(bit) + npy.mod(len(bit), 8))

    # To string and remove white spaces
    a = array2String(bit)
    a = a.replace(" ", "")

    # Start from last bits to avoid problems with 0
    characterOut = ""
    for i in range(len(a) // 8):
        if i == 0:
            charbit = a[len(a) - 8:]
        else:
            charbit = a[-(i + 1) * 8: -i * 8]
        charbit = int(charbit, 2)
        characterOut = charbit.to_bytes((charbit.bit_length() + 7) // 8, "big").decode("utf-8",
                                                                                       errors="ignore") + characterOut
    return characterOut
