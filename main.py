import sys
from datetime import datetime
from os.path import exists

import argparse
from argparse import RawTextHelpFormatter

import numpy as npy
from imports.NTRUEncrypt import NTRUEncrypt
from imports.NTRUDecrypt import NTRUDecrypt
from imports.Utilities import *

# Add input arguments
prs = argparse.ArgumentParser(prog="NTRUEncrypt & NTRUDecrypt", formatter_class=RawTextHelpFormatter)
prs.add_argument("-k", "--key_name", default="ntru", type=str, help="Filename of the public and private keys.\n")
prs.add_argument("-g", "--key_gen", action="store_true", help="Generate the public and private key files.\n")
prs.add_argument("-S4", "--S4", action="store_true",
                 help="Generate high security keys with size optimized.\n")
prs.add_argument("-S3", "--S3", action="store_true",
                 help="Generate moderate security keys with size optimized.\n")
prs.add_argument("-S2", "--S2", action="store_true",
                 help="Generate low security keys with size optimized.\n")
prs.add_argument("-S1", "--S1", action="store_true",
                 help="Generate lowest security keys with size optimized.\n")
prs.add_argument("-C4", "--C4", action="store_true",
                 help="Generate high security keys with cost optimized.\n")
prs.add_argument("-C3", "--C3", action="store_true",
                 help="Generate moderate security keys with cost optimized.\n")
prs.add_argument("-C2", "--C2", action="store_true",
                 help="Generate low security keys with cost optimized.\n")
prs.add_argument("-C1", "--C1", action="store_true",
                 help="Generate lowest security keys with cost optimized.\n")
prs.add_argument("-F4", "--F4", action="store_true",
                 help="Generate high security keys with speed optimized.\n")
prs.add_argument("-F3", "--F3", action="store_true",
                 help="Generate moderate security keys with speed optimized.\n")
prs.add_argument("-F2", "--F2", action="store_true",
                 help="Generate low security keys with speed optimized.\n")
prs.add_argument("-F1", "--F1", action="store_true",
                 help="Generate lowest security keys with speed optimized.\n")
prs.add_argument("-N", "--N", default=1499, type=int, help="The order of the polynomial ring. Default is 1499.\n")
prs.add_argument("-p", "--p", default=3, type=int, help="The smallest inverse polynomial modulus. Default is 3.\n")
prs.add_argument("-q", "--q", default=2048, type=int, help="The largest inverse polynomial modulus. Default is 2048.\n")
prs.add_argument("-df", "--df", default=499, type=int, help="Polynomial f has df 1's and df -1's. Default is 499.\n")
prs.add_argument("-dg", "--dg", default=79, type=int, help="Polynomial g has dg 1's and -1's. Default is 79.\n")
prs.add_argument("-dr", "--dr", default=79, type=int,
                 help="Random polynomial has d 1's and -1's. Default 79.\n")
prs.add_argument("-of", "--out_file", type=str, help="Output file for encrypted/decrypted data/string.\n")
prs.add_argument("-ot", "--out_term", action="store_true",
                 help="Output encrypted/decrypted data/string to terminal.\n")
prs.add_argument("-estr", "--en_str", type=str, help="Encrypt the string given as an input.\n")
prs.add_argument("-efile", "--en_file", type=str, help="Encrypt the string given in this input file.\n")
prs.add_argument("-dstr", "--de_str", type=str, help="Decrypt the string given as an input.\n")
prs.add_argument("-dfile", "--de_file", type=str, help="Decrypt the string given in this input file.\n")

args = prs.parse_args()
if __name__ == "__main__":
    # Generate public and private keys with input flags
    if args.key_gen:
        a = NTRUDecrypt()

        # Set parameters
        if args.S1:
            a.setVariables(N=401, p=3, q=2048, df=133, dg=133, dr=133)
        elif args.S2:
            a.setVariables(N=449, p=3, q=2048, df=149, dg=134, dr=134)
        elif args.S3:
            a.setVariables(N=677, p=3, q=2048, df=225, dg=157, dr=157)
        elif args.S4:
            a.setVariables(N=1087, p=3, q=2048, df=361, dg=120, dr=120)
        elif args.C1:
            a.setVariables(N=541, p=3, q=2048, df=180, dg=49, dr=49)
        elif args.C2:
            a.setVariables(N=613, p=3, q=2048, df=204, dg=55, dr=55)
        elif args.C3:
            a.setVariables(N=887, p=3, q=2048, df=295, dg=81, dr=81)
        elif args.C4:
            a.setVariables(N=1171, p=3, q=2048, df=390, dg=106, dr=106)
        elif args.F1:
            a.setVariables(N=659, p=3, q=2048, df=219, dg=38, dr=38)
        elif args.F2:
            a.setVariables(N=761, p=3, q=2048, df=253, dg=42, dr=42)
        elif args.F3:
            a.setVariables(N=1087, p=3, q=2048, df=362, dg=63, dr=63)
        else:
            a.setVariables(N=1499, p=3, q=2048, df=499, dg=79, dr=79)

        start = datetime.now()
        a.genPubPri(args.key_name)
        print('Time generating both keys: ', datetime.now() - start)
        print("\n")
        start = 0

        # Encrypt data using given public key
    elif args.en_str or args.en_file:
        # Check if public key exists
        if not exists(args.key_name + ".pub"):
            sys.exit("Error : Public key '" + args.key_name + ".pub' not found.")

        # One input to encrypt
        if args.en_str and args.en_file:
            sys.exit("Error : More than one input is given.")

        # Output method specified
        if not args.out_file and not args.out_term:
            sys.exit("Error : Missing output method.")

        # Initialise encryption class
        b = NTRUEncrypt()

        # Read public key
        start = datetime.now()
        b.readpubK(args.key_name + ".pub")

        # Extract data to encrypt
        if args.en_str:
            to_encrypt = args.en_str
        elif args.en_file:
            # Check if the file exists
            if not exists(args.en_file):
                sys.exit("Error : Input file '" + args.en_file + "' not found.")
            # If it does then read all the data from it
            with open(args.en_file, "r") as f:
                to_encrypt = "".join(f.readlines())

        # Encrypt data
        b.encryptString(to_encrypt)
        print('Time encrypting data: ', datetime.now() - start)
        print("\n")
        start = 0

        # Output the encrypted data
        if args.out_term:
            print(b.saveM)
        elif args.out_file:
            # Write data to output file
            with open(args.out_file, "w") as f:
                f.write(b.saveM)

    # Decrypt data from private key
    elif args.de_str or args.de_file:

        # Check if the private key file exists
        if not exists(args.key_name + ".pri"):
            sys.exit("Error : Public key '" + args.key_name + ".pri' not found.")

        # One input to decrypt only
        if args.de_str and args.de_file:
            sys.exit("Error : More than one input to decrypt given.")

        # We need an output method specified
        if not args.out_file and not args.out_term:
            sys.exit("Error : At least one output method must be specified.")

        # Then initialise a decryption class
        D = NTRUDecrypt()

        # And read the public key
        start = datetime.now()
        D.readPri(args.key_name + ".pri")

        # Extract the data to decrypt
        if args.de_str:
            to_decrypt = args.de_str
        elif args.de_file:
            # Need to check if the file exists
            if not exists(args.de_file):
                sys.exit("Error : Input file '" + args.de_file + "' not found.")
            # If it does then read all the data from it
            with open(args.de_file, "r") as f:
                to_decrypt = "".join(f.readlines())

        # Then decrypt the string
        D.decryptString(to_decrypt)
        print('Time decrypting data: ', datetime.now() - start)
        print("\n")
        start = 0

        # And output the decrypted data
        if args.out_term:
            print(D.saveM)
        elif args.out_file:
            # Write data to output file
            with open(args.out_file, "w") as f:
                f.write(D.saveM)
