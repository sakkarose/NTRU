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
prs.add_argument("-k", default="ntru", type=str, help="Filename of the public and private keys.\n")
prs.add_argument("-g", "--gen", action="store_true", help="Generate the public and private key files.\n")
prs.add_argument("-S4", action="store_true",
                 help="Generate high security keys with size optimized.\n")
prs.add_argument("-S3", action="store_true",
                 help="Generate moderate security keys with size optimized.\n")
prs.add_argument("-S2", action="store_true",
                 help="Generate low security keys with size optimized.\n")
prs.add_argument("-S1", action="store_true",
                 help="Generate lowest security keys with size optimized.\n")
prs.add_argument("-C4", action="store_true",
                 help="Generate high security keys with cost optimized.\n")
prs.add_argument("-C3", action="store_true",
                 help="Generate moderate security keys with cost optimized.\n")
prs.add_argument("-C2", action="store_true",
                 help="Generate low security keys with cost optimized.\n")
prs.add_argument("-C1", action="store_true",
                 help="Generate lowest security keys with cost optimized.\n")
prs.add_argument("-F4", action="store_true",
                 help="Generate high security keys with speed optimized.\n")
prs.add_argument("-F3", action="store_true",
                 help="Generate moderate security keys with speed optimized.\n")
prs.add_argument("-F2", action="store_true",
                 help="Generate low security keys with speed optimized.\n")
prs.add_argument("-F1", action="store_true",
                 help="Generate lowest security keys with speed optimized.\n")
prs.add_argument("-N", "--N", default=1499, type=int, help="The order of the polynomial ring. Default is 1499.\n")
prs.add_argument("-p", "--p", default=3, type=int, help="The smallest inverse polynomial modulus. Default is 3.\n")
prs.add_argument("-q", "--q", default=2048, type=int, help="The largest inverse polynomial modulus. Default is 2048.\n")
prs.add_argument("-df", "--df", default=499, type=int, help="Polynomial f has df 1's and df -1's. Default is 499.\n")
prs.add_argument("-dg", "--dg", default=79, type=int, help="Polynomial g has dg 1's and -1's. Default is 79.\n")
prs.add_argument("-dr", "--dr", default=79, type=int,
                 help="Random polynomial has d 1's and -1's. Default 79.\n")
prs.add_argument("-O", "--out_file", type=str, help="Output file for encrypted/decrypted data/string.\n")
prs.add_argument("-T", "--out_term", action="store_true",
                 help="Output encrypted/decrypted data/string to terminal.\n")
# String must be given in quotation marks for -eS and -dS
# -dS and -dF require a known public key
prs.add_argument("-eS", "--Enc_string", type=str, help="Encrypt the string given as an input.\n")
prs.add_argument("-eF", "--Enc_file", type=str, help="Encrypt the string given in this input file.\n")
prs.add_argument("-dS", "--Dec_string", type=str, help="Decrypt the string given as an input.\n")
prs.add_argument("-dF", "--Dec_file", type=str, help="Decrypt the string given in this input file.\n")

args = prs.parse_args()
if __name__ == "__main__":
    # Generate public and private keys with input flags
    if args.Gen:
        start = datetime.now()
        a = NTRUDecrypt()

        # Set parameters
        if args.S1:
            a.setVariables(N=401, p=3, q=2048, df=15, dg=12, dr=2048)
        elif args.S2:
            a.setVariables(N=503, p=3, q=2048, df=216, dg=72, dr=2048)
        elif args.S3:
            a.setVariables(N=503, p=3, q=2048, df=216, dg=72, dr=2048)
        elif args.S4:
            a.setVariables(N=503, p=3, q=2048, df=216, dg=72, dr=2048)
        elif args.C1:
            a.setVariables(N=503, p=3, q=2048, df=216, dg=72, dr=2048)
        elif args.C2:
            a.setVariables(N=503, p=3, q=2048, df=216, dg=72, dr=2048)
        elif args.C3:
            a.setVariables(N=503, p=3, q=2048, df=216, dg=72, dr=2048)
        elif args.C4:
            a.setVariables(N=503, p=3, q=2048, df=216, dg=72, dr=2048)
        elif args.F1:
            a.setVariables(N=503, p=3, q=2048, df=216, dg=72, dr=2048)
        elif args.F2:
            a.setVariables(N=503, p=3, q=2048, df=216, dg=72, dr=2048)
        elif args.F3:
            a.setVariables(N=503, p=3, q=2048, df=216, dg=72, dr=2048)
        else:
            a.setVariables(N=167, p=3, q=2048, df=61, dg=20, dr=2048)

        a.genPubPri(args.key_name)
        print('Time generating both keys: ', datetime.now() - start)
        start = 0

        # Encrypt data using given public key
    elif args.Enc_string or args.Enc_file:
        # Check if public key exists
        if not exists(args.key_name + ".pub"):
            sys.exit("Error : Public key '" + args.key_name + ".pub' not found.")

        # One input to encrypt
        if args.Enc_string and args.Enc_file:
            sys.exit("Error : More than one input is given.")

        # Output method specified
        if not args.out_file and not args.out_in_term:
            sys.exit("Error : Missing output method.")

        start = datetime.now()
        # Initialise encryption class
        b = NTRUEncrypt()

        # Read public key
        b.readpubK(args.key_name + ".pub")

        # Extract data to encrypt
        if args.Enc_string:
            to_encrypt = args.Enc_string
        elif args.Enc_file:
            # Check if the file exists
            if not exists(args.Enc_file):
                sys.exit("Error : Input file '" + args.Enc_file + "' not found.")
            # If it does then read all the data from it
            with open(args.Enc_file, "r") as f:
                to_encrypt = "".join(f.readlines())

        # Encrypt data
        b.encryptString(to_encrypt)
        print('Time encrypting data: ', datetime.now() - start)
        start = 0

        # Output the encrypted data
        if args.out_in_term:
            print(b.saveM)
        elif args.out_file:
            # Write data to output file
            with open(args.out_file, "w") as f:
                f.write(b.saveM)

    # Decrypt data from private key
    elif args.Dec_string or args.Dec_file:

        # Check if the private key file exists
        if not exists(args.key_name + ".pri"):
            sys.exit("Error : Public key '" + args.key_name + ".pri' not found.")

        # One input to decrypt only
        if args.Dec_string and args.Dec_file:
            sys.exit("Error : More than one input to decrypt given.")

        # We need an output method specified
        if not args.out_file and not args.out_in_term:
            sys.exit("Error : At least one output method must be specified.")

        start = datetime.now()
        # Then initialise a decryption class
        D = NTRUDecrypt()

        # And read the public key
        D.readPri(args.key_name + ".pri")

        # Extract the data to decrypt
        if args.Dec_string:
            to_decrypt = args.Dec_string
        elif args.Dec_file:
            # Need to check if the file exists
            if not exists(args.Dec_file):
                sys.exit("Error : Input file '" + args.Dec_file + "' not found.")
            # If it does then read all the data from it
            with open(args.Dec_file, "r") as f:
                to_decrypt = "".join(f.readlines())

        # Then decrypt the string
        D.decryptString(to_decrypt)
        print('Time decrypting data: ', datetime.now() - start)
        start = 0

        # And output the decrypted data
        if args.out_in_term:
            print(D.saveM)
        elif args.out_file:
            # Write data to output file
            with open(args.out_file, "w") as f:
                f.write(D.saveM)
