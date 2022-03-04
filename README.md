# NTRU
Just a simple implementation of **NTRU** which is one of the **Round-3 Finalists of Post-Quantum Cryptography** in **Public-key Encryption and Key-establishment Algorithms**.

For simple implementation, `sympy` is used for polynomial. So for the larger polynomial rings, this might needs more works. `numpy` is also needed for many things to run this.

This is just for studying purposes so the code can be unoptimized and outputs will be uncompressed. Do not use this for actual cryptographic uses.

At the moment, there is only **NTRUEncrypt** (& **NTRUDecrypt**), **NTRUSign** might be there any time soon.

- This program is still not finished yet, I'm fixing minor stuffs and trying the post-quantum security parameters which are suggested from **IEEE p1363.1 Standard** [1].
- This is only just PKE, I will start on KEM later.

- More details will be added when this one is finished.

[1] : T. Kim and M. -K. Lee, "Efficient and Secure Implementation of NTRUEncrypt Using Signed Sliding Window Method," in IEEE Access, vol. 8, pp. 126591-126605, 2020, doi: 10.1109/ACCESS.2020.3008182.

