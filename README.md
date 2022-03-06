# NTRU
## Introduction
Just a simple implementation of **NTRU** which is one of the **Round-3 Finalists of Post-Quantum Cryptography** in **Public-key Encryption and Key-establishment Algorithms**. For the same reason, `sympy` is used for polynomial. So for the larger polynomial rings, this might needs more works. `numpy` is also needed for many things to run this. This is just for studying purposes so the code can be unoptimized and outputs will be uncompressed. Do not use this for actual cryptographic uses and also the post-quantum security parameters are suggested from **IEEE p1363.1 Standard** [1].

At the moment, there is only **NTRUEncrypt** (& **NTRUDecrypt**), **NTRUSign** might be there any time soon.

## Installation
- No installation needed, but you need to have `sympy` and `numpy` in python.
- After that you can run the program by executing the `main.py` file .
- Also pypy3 is optional.

## Parameters [2]

- High security
  - `-S4`  : Optimized for size.
  - `-C4`  : Optimized for cost.
  - `-F4`  : Optimized for speed.
- Moderate security : `-S3`, `-C3`, `-F3`
- Low security : `-S2`, `-C2`, `-F2`
- Lowest security : `-S1`, `-C1`, `-F1`

- If you don't pick parameter, it will use the default parameter which is `F4`.

| Parameter Set  | N | p | q | dg  | df | dr  |
| :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **(S1)** ees401ep1  | 401  | 3  | 2048  | 133  | 113  | 113  |
| **(S2)** ees449ep1  | 449  | 3  | 2048  | 149  | 134  | 134  |
| **(S3)** ees677ep1  | 677  | 3  | 2048  | 225  | 157  | 157  |
| **(S4)** ees1087ep2  | 1087  | 3  | 2048  | 362  | 120  | 120  |
| **(C1)** ees541ep1  | 541  | 3  | 2048  | 180  | 49  | 49  |
| **(C2)** ees613ep1  | 613  | 3  | 2048  | 204  | 55  | 55  |
| **(C3)** ees887ep1  | 887  | 3  | 2048  | 295  | 81  | 81  |
| **(C4)** ees1171ep1  | 1171  | 3  | 2048  | 390  | 106  | 106  |
| **(F1)** ees659ep1  | 659  | 3  | 2048  | 219  | 38  | 38  |
| **(F2)** ees761ep1  | 761  | 3  | 2048  | 253  | 42  | 42  |
| **(F3)** ees1087ep1  | 1087  | 3  | 2048  | 362  | 63  | 63  |
| **(F4)** ees1499ep1  | 1499  | 3  | 2048  | 499  | 79  | 79  |

## Generating Key
- To generate keys. We run the `main.py` with parameter `-g`.
- To change file name of the keys. We add parameter `-k`. (Default is `ntru`).
### Example
- To generate public and private keys with high security, optimized for speed and named "test_key".
```
python3 main.py -F4 -g -k test_key
```
- To generate keys with your own parameters.
```
python3 main.py -g -N 1499 -p 3 -q 2048 -dg 499 -df 79 -dr 79
```
## Encrypting
- To encrypt a string, use `-esr`, and `-efi` for a file
- To define the output, you can use `-of` to write it in a file, and `-ot` will print the output to the screen.
### Example
- To encrypt a string "Hello" with key named "test_key" and print the output on the screen.
```
python3 main.py -k test_key -esr "Hello" -ot
```
- To encrypt a file named "Hi.txt" with key named "test_key" and write it in the file named "post_hi.bin"
```
python3 main.py -k test_key -efi Hi.txt -of post_hi.bin
```
## Decrypting
- Same for encrypting, we have `-dsr` for a string and `-dfi` for a file.
- Both `-of` and `-ot`are also working for decrypting too.
### Example
- To decrypt a string "Hello" with key named "test_key" and print the output on the screen.
```
python3 main.py -k test_key -es "Hello" -ot
```
- To decrypt a file named "Hi.txt" with key named "test_key" and write it in the file named "post_hi.bin"
```
python3 main.py -k test_key -ef Hi.txt -of post_hi.bin
```
## Notes
- This is only just PKE, I will start on KEM later.
- More details will be added when this one is finished.

## References
[1](https://ieeexplore.ieee.org/document/4800404) : "IEEE Standard Specification for Public Key Cryptographic Techniques Based on Hard Problems over Lattices," in IEEE Std 1363.1-2008 , vol., no., pp.1-81, 10 March 2009, doi: 10.1109/IEEESTD.2009.4800404.

[2](https://ieeexplore.ieee.org/document/9137237) : T. Kim and M. -K. Lee, "Efficient and Secure Implementation of NTRUEncrypt Using Signed Sliding Window Method," in IEEE Access, vol. 8, pp. 126591-126605, 2020, doi: 10.1109/ACCESS.2020.3008182.

