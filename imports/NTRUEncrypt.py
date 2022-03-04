import sys

import numpy as npy
from sympy import Poly, symbols
from imports.Utilities import *


class NTRUEncrypt:
    def __init__(self, N=503, p=3, q=256, dr=18):
        # Public N, p and q
        self.N = N
        self.p = p
        self.q = q

        # Number of 1s in r
        self.oneofr = dr

        # Private key polynomial g
        self.g = npy.zeros((self.N,), dtype=int)

        # Public key polynomial h (mod q)
        self.h = npy.zeros((self.N,), dtype=int)

        # Random value
        self.r = npy.zeros((self.N,), dtype=int)
        self.generateRandomPoly()

        # Message
        self.m = npy.zeros((self.N,), dtype=int)

        # Encrypted message
        self.e = npy.zeros((self.N,), dtype=int)

        # Representing polynomial
        self.I = npy.zeros((self.N + 1,), dtype=int)
        self.I[self.N] = -1
        self.I[0] = 1

        # Boolean value check if we have read the public key file or not
        self.readKey = False

        # Save encrypted messages if needed as string
        self.saveM = None

    # Read the public key file, generate new r based on new N
    def readpubK(self, filename="key.pub"):
        with open(filename, "r") as o:
            self.p = int(o.readline().split(" ")[-1])
            self.q = int(o.readline().split(" ")[-1])
            self.N = int(o.readline().split(" ")[-1])
            self.oneofr = int(o.readline().split(" ")[-1])
            self.h = npy.zeros((self.N + 1,), dtype=int)
        self.I = npy.zeros((self.N + 1,), dtype=int)
        self.I[self.N] = -1
        self.I[0] = 1
        self.generateRandomPoly()
        self.readKey = True

    # Generate random polynomial array r, with mod q
    def generateRandomPoly(self):
        self.r = generateRandom1n0(self.N, self.oneofr, self.oneofr)

    # Suitable checks on message, then set it
    def setMessageM(self, M):
        if not self.readKey:
            sys.exit("Error : Public key didn't read before this")
        if len(M) > self.N:
            sys.exit("Error : Message length longer than degree of polynomial ring")
        for i in range(len(M)):
            if M[i] < -self.p / 2 or M[i] > self.p / 2:
                sys.exit("Error : Elements of message aren't in [-p/2, p/2]")
        # Set the message
        self.m = padArray(M, self.N)

    def ntruEncrypt(self, m=None):
        if not self.readKey:
            sys.exit("Error : Reading public key file has to be done before this")
        #
        if m is not None:
            if len(m) > self.N:
                sys.exit("\n\nError : Polynomial message of degree >= N")
            self.m = m
        x = symbols('x')
        # Encrypting part
        self.e = npy.array(
            ((((Poly(self.r, x) * Poly(self.h, x)).trunc(self.q)) + Poly(self.m, x)) % Poly(self.I, x)).trunc(
            self.q).all_coeffs(), dtype=int)
        self.e = padArray(self.e, self.N)

    def encryptString(self, M):
        if not self.readKey:
            sys.exit("Error : Reading public key has to be done first")
        # Create binary array of message string, pad it with leading 0
        binaryArray = string2Bit(M)
        binaryArray = padArray(binaryArray, len(binaryArray) - npy.mod(len(binaryArray), self.N) + self.N)

        # Empty string
        self.saveM = ""

        # Each message block (length N) will be encrypted with different random polynomial
        for E in range(len(binaryArray // self.N)):
            self.generateRandomPoly()
            # Message will be encrypted as single block
            self.setMessageM(binaryArray[E * self.N: (E + 1) * self.N])
            # Encrypt the message
            self.ntruEncrypt()
            # Put encrypted message to string
            self.saveM = self.saveM + array2String(self.e) + " "
