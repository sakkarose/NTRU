import sys
import numpy as npy
from math import log, gcd
from sympy import Poly, symbols
from imports.Utilities import *


class NTRUDecrypt:
    def __init__(self, N=503, p=3, q=256, df=61, dg=20, dr=18):

        # Public N, order of the polynomial ring
        self.N = N
        # Public p, mod of inverse of f polynomial for fp
        self.p = p
        # Public q, mod of inverse of f polynomial for fq
        self.q = q

        # Number of coefficients 1 in polynomial f
        self.df = df
        # Number of coefficients 1 in polynomial g
        self.dg = dg
        # Number of coefficients 1 in random polynomial r
        self.oneofr = dr

        # Private polynomial f
        self.f = npy.zeros((self.N,), dtype=int)
        # Inverse of f mod p
        self.fp = npy.zeros((self.N,), dtype=int)
        # Inverse of f mod q
        self.fq = npy.zeros((self.N,), dtype=int)
        # Private polynomial g
        self.g = npy.zeros((self.N,), dtype=int)
        # Public key polynomial (mod q)
        self.h = npy.zeros((self.N,), dtype=int)

        # Representing polynomial
        self.I = npy.zeros((self.N + 1,), dtype=int)
        self.I[self.N] = -1
        self.I[0] = 1

        # Empty string for decrypted string
        self.saveM = None

    # Set variables. N, p, q will be checked
    def setVariables(self, N=None, p=None, q=None, df=None, dg=None, dr=None):
        #
        if N is not None:
            # Check if N is prime
            if not primeCheck(N):
                sys.exit("\n\nError : N isn't prime")
            else:
                # Error checks based on 1 and -1 of df, dg and dr arrays
                if df is None:
                    if 2 * self.df > N:
                        sys.exit("\n\nError : N too small")
                if dg is None:
                    if 2 * self.dg > N:
                        sys.exit("\n\nError : N too small")
                if dr is None:
                    if 2 * self.oneofr > N:
                        sys.exit("\n\nError : N too small")
                # If N is okay, initialise the polynomial arrays
                self.N = N
                self.f = npy.zeros((self.N,), dtype=int)
                self.fp = npy.zeros((self.N,), dtype=int)
                self.fq = npy.zeros((self.N,), dtype=int)
                self.g = npy.zeros((self.N,), dtype=int)
                self.h = npy.zeros((self.N,), dtype=int)
                self.I = npy.zeros((self.N + 1,), dtype=int)
                self.I[self.N] = -1
                self.I[0] = 1

        # Set p and q together
        if (p is None and q is not None) or (p is not None and q is None):
            sys.exit("\n\nError : p and q aren't together")
        elif p is not None and q is not None:
            if (8 * p) > q:
                sys.exit("\n\nError : 8p <= q required")
            else:
                if gcd(p, q) != 1:
                    sys.exit("\n\nError : p and q aren't co-prime\n\n")
                else:
                    self.p = p
                    self.q = q

        if df is not None:
            if 2 * df > self.N:
                sys.exit("\n\nError : df is needed to be 2 * df > N\n\n")
            else:
                self.df = df

        if dg is not None:
            if 2 * dg > self.N:
                sys.exit("\n\nError : dg is needed to be 2 * dg > N\n\n")
            else:
                self.dg = dg

        if dr is not None:
            if 2 * d > self.N:
                sys.exit("\n\nError : dr is needed to be 2 * dr > N\n\n")
            else:
                self.oneofr = dr

    # Invert the f polynomial with p and q
    def invertf(self):
        fp_temp = polynomialInverse(self.f, self.I, self.p)
        fq_temp = polynomialInverse(self.f, self.I, self.q)
        if len(fp_temp) > 0 and len(fq_temp) > 0:
            self.fp = npy.array(fp_temp)
            self.fq = npy.array(fq_temp)
            # Check if arrays have leading zeros
            if len(self.fp) < self.N:
                self.fp = npy.concatenate([npy.zeros(self.N - len(self.fp), dtype=int), self.fp])
            if len(self.fq) < self.N:
                self.fq = npy.concatenate([npy.zeros(self.N - len(self.fq), dtype=int), self.fq])
            return True
        else:
            return False

    # Generate random f and g for private key and inverses
    def generatefandg(self):
        # Exit if can't find inverse
        maxTries = 100
        # Generate random g
        self.g = generateRandom1n0(self.N, self.dg, self.dg)
        # Generate f with inverses mod p and mod q
        for i in range(maxTries):
            self.f = generateRandom1n0(self.N, self.df, self.df - 1)
            invf_try = self.invertf()
            if invf_try:
                break
            elif i == maxTries - 1:
                sys.exit("Couldn't generate inverses of f")

    # Generate public key from values
    def genPub(self):
        x = symbols('x')
        self.h = Poly((Poly(self.p * self.fq, x).trunc(self.q) * Poly(self.g, x)).trunc(self.q)
                      % Poly(self.I, x)).all_coeffs()

    # Write public key
    def writePub(self, filename="key"):
        pubHead = "p ::: " + str(self.p) + "\nq ::: " + str(self.q) + "\nN ::: " + str(self.N) + "\ndr ::: " + str(
            self.oneofr) + "\nh :::"
        npy.savetxt(filename + ".pub", self.h, newline=" ", header=pubHead, fmt="%s")

    # Read public key
    def readPub(self, filename="key.pub"):
        with open(filename, "r") as f:
            self.p = int(f.readline().split(" ")[-1])
            self.q = int(f.readline().split(" ")[-1])
            self.N = int(f.readline().split(" ")[-1])
            self.oneofr = int(f.readline().split(" ")[-1])
            self.h = npy.array(f.readline().split(" ")[3:-1], dtype=int)
        self.I = npy.zeros((self.N + 1,), dtype=int)
        self.I[self.N] = -1
        self.I[0] = 1

    # Write private key
    def writePri(self, filename="key"):
        priHead = "p ::: " + str(self.p) + "\nq ::: " + str(self.q) + "\nN ::: " + str(self.N) + "\ndf ::: " + str(
            self.df) + "\ndg ::: " + str(self.dg) + "\ndr ::: " + str(self.oneofr) + "\nf/fp/fq/g :::"
        npy.savetxt(filename + ".pri", (self.f, self.fp, self.fq, self.g), header=priHead, newline="\n", fmt="%s")

    # Read private key
    def readPri(self, filename="key.pri"):
        with open(filename, "r") as f:
            self.p = int(f.readline().split(" ")[-1])
            self.q = int(f.readline().split(" ")[-1])
            self.N = int(f.readline().split(" ")[-1])
            self.df = int(f.readline().split(" ")[-1])
            self.dg = int(f.readline().split(" ")[-1])
            self.oneofr = int(f.readline().split(" ")[-1])

            temp = f.readline()

            self.f = npy.array(f.readline().split(" "), dtype=int)
            self.fp = npy.array(f.readline().split(" "), dtype=int)
            self.fq = npy.array(f.readline().split(" "), dtype=int)
            self.g = npy.array(f.readline().split(" "), dtype=int)
        self.I = npy.zeros((self.N + 1,), dtype=int)
        self.I[self.N] = -1
        self.I[0] = 1

    # Generate public and private keys from N, p and q
    def genPubPri(self, keyfileName="key"):
        self.generatefandg()
        self.genPub()
        self.writePub(keyfileName)
        self.writePri(keyfileName)

    # Decrypt message
    def ntruDecrypt(self, e):
        # Encrypted message e must have degree < N
        if len(e) > self.N:
            sys.exit("Encrypted message has degree > N")
        # If there is no error, continue to decrypt and return as a numpy array
        x = symbols('x')
        a = ((Poly(self.f, x) * Poly(e, x)) % Poly(self.I, x)).trunc(self.q)
        b = a.trunc(self.p)
        c = ((Poly(self.fp, x) * b) % Poly(self.I, x)).trunc(self.p)

        return npy.array(c.all_coeffs(), dtype=int)

    # Decrypt the message using public key from encoded to decoded string
    def decryptString(self, E):
        # Convert string to a numpy
        Me = npy.fromstring(E, dtype=int, sep=' ')
        # Check input has the same length
        if npy.mod(len(Me), self.N) != 0:
            sys.exit("\n\nError : Incorrect input length")

        # Decrypt each block, append it to message string
        Marray = npy.array([], dtype=int)
        for D in range(len(Me) // self.N):
            Marray = npy.concatenate((Marray, padArray(self.ntruDecrypt(Me[D * self.N:(D + 1) * self.N]), self.N)))

        # Return the decrypted string
        self.saveM = bit2String(Marray)
