import decimal
from fractions import Fraction

decimal.getcontext().prec = 10_00_000

"""TODO:
        implement gcd and eea
"""


def gcd(e, r):
    while r != 0:
        e, r = r, e % r
    return e


# Extended Euclidean Algorithm
def eea(a, b):
    if a % b == 0:
        return (b, 0, 1)
    else:
        gcd, s, t = eea(b, a % b)
        s = s - ((a // b) * t)
        return (gcd, t, s)


"""TODO:
        1. p and q of the form 4k+3
        2. n = p^2 * q --> public key
        3. (p,q) --> pvt key
"""


def key_generation(p, q):
    public_key = (p ** 2) * q
    pvt_key = (p, q)
    return public_key, pvt_key


"""TODO:
        C = M^2 mod n
"""


def encryption(public_key, message):
    n = public_key
    enc_text = (message ** 2) % public_key
    return enc_text


def decryption(public_key, pvt_key, enc_text):
    p, q = pvt_key
    # form an equation ap + bq = 1
    # a possible solution is 1/2p and 1/2q
    gcd, a, b = eea(p, q)
    p = decimal.Decimal(p)
    q = decimal.Decimal(q)
    a = decimal.Decimal(a)
    b = decimal.Decimal(b)
    print(((p + 1)) / 4)
    R = (enc_text ** ((p + 1) / 4)) % p
    S = (enc_text ** ((q + 1) / 4)) % q

    m1 = int((a * p * S) + (b * q * R)) % int(p * q)
    m2 = int((a * p * S) - (b * q * R)) % int(p * q)
    m3 = (-1 * m2) % int(p * q)
    m4 = (-1 * m1) % int(p * q)
    message = [m1, m2, m3, m4]
    w = list()
    w.append(((enc_text - m1 ** 2) / public_key))
    w.append((enc_text - m2 ** 2) / public_key)
    w.append((enc_text - m3 ** 2) / public_key)
    w.append((enc_text - m4 ** 2) / public_key)
    for i, weight in enumerate(w):
        if weight % 1 == 0:
            return message[i]


p = int(input("Enter p of the form 4k + 3: "))
q = int(input("Enter q of the form 4k + 3: "))
message = int(input("Input the message to be sent with the range of Zpq: "))
public_key, pvt_key = key_generation(p, q)
enc_text = encryption(public_key, message)
print("Encrypted text is:", enc_text)
message = decryption(public_key, pvt_key, enc_text)
print("The Decrypted texts is:")
print(message)
