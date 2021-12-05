import random
import math
from utils.tools import gcd, mult_inv


def pub_exp(totient):
    e_list = list()

    for i in range(2, totient):
        if gcd(i, totient) == 1:
            e_list.append(i)

    e = random.choice(e_list)
    e = e_list[4]

    return e


def pvt_exp(e, totient):
    return mult_inv(e, totient)


def encrypt(msg, n, e):
    print("Value of E is:", e)
    ct = math.pow(msg, e) % n

    return ct


def decrypt(ct, n, d):
    print("Value of D is:", d)
    pt = math.pow(int(ct), d) % n

    return pt
