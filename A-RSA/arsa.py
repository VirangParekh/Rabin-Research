import random

# from mathTools.tools import
# GCD based on Euclid's Algorithm


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


# Multiplicative Inverse


def mult_inv(e, r):
    gcd, s, _ = eea(e, r)
    if gcd != 1:
        return None
    else:
        return s % r


# rsa encryption


def rsa_encrypt(pub_key, text):
    n, e = pub_key
    result = list()
    index = 0
    for i in text:
        index = ord(i)
        c = (index ** e) % n
        result.append(c)
        # print(i,c)
    return result


# rsa decryption
"""DECRYPTION ALGORITHM"""


def rsa_decrypt(priv_key, c_text):
    n, d = priv_key
    txt = c_text
    x = ""
    index = 0
    for i in txt:
        index = (int(i) ** d) % n
        # print(index)
        c = chr(index)
        x += c
    return x


def key_generation(p, q):
    public_key = p * q
    pvt_key = (p, q)
    return public_key, pvt_key


def encryption(public_key, message):
    n = public_key
    enc_text = (message ** 2) % public_key
    return enc_text


def decryption(public_key, pvt_key, enc_text):
    p, q = pvt_key
    # form an equation ap + bq = 1
    # a possible solution is 1/2p and 1/2q
    gcd, a, b = eea(p, q)
    R = (enc_text ** ((p + 1) / 4)) % p
    S = (enc_text ** ((q + 1) / 4)) % q
    m1 = ((a * p * S) + (b * q * R)) % public_key
    m2 = public_key - m1
    m3 = ((a * p * S) - (b * q * R)) % public_key
    m4 = public_key - m3
    return m1, m2, m3, m4


# Main Function
print("Enter two prime numbers p and q")
p = int(input("Enter p: "))
q = int(input("Enter q: "))
n = p * q
totient = (p - 1) * (q - 1)
print(p, q, n, totient)

# e Value Calculation
e_list = list()
for i in range(2, totient):
    if gcd(i, totient) == 1:
        e_list.append(i)
e = random.choice(e_list)
# e = e_list[4]
# print(e_list)
print("The value of e is: ", e)

# d value calculation
d = mult_inv(e, totient)
print("The value of d is: ", d)

# rsa pk and pvtk

privat_key = [n, d]
public_key = [n, e]

print("public and private key are: ", public_key, privat_key)
message = input("Enter Message: ")
cipher_text = rsa_encrypt(public_key, message)
print("Cipher text after rsa is : ", cipher_text)

p2 = int(input("Enter p of the form 4k + 3: "))
q2 = int(input("Enter q of the form 4k + 3: "))
r = random.randint(2, p2 * q2)
print("Random Number is: ", r)
public_key2, pvt_key2 = key_generation(p2, q2)
# encrypt r in rabin
r1 = encryption(public_key2, r)
print("Ciphered Key for rabin is: ", r1)
xor_cipher_text = list()
for i in cipher_text:
    xor_cipher_text.append(i ^ r)
print("Cipher text after xor", xor_cipher_text)

cipher_text = input("Enter cipher text: ")
r2 = int(input("Enter ciphered key: "))
m1, m2, m3, m4 = decryption(public_key2, pvt_key2, r2)
cipher_text_before_xor1 = list()
cipher_text_before_xor2 = list()
cipher_text_before_xor3 = list()
cipher_text_before_xor4 = list()

cipher_text = cipher_text.split(",")
for i in cipher_text:
    cipher_text_before_xor1.append(int(i) ^ int(m1))
for i in cipher_text:
    cipher_text_before_xor2.append(int(i) ^ int(m2))
for i in cipher_text:
    cipher_text_before_xor3.append(int(i) ^ int(m3))
for i in cipher_text:
    cipher_text_before_xor4.append(int(i) ^ int(m4))

plain_text = rsa_decrypt(privat_key, cipher_text_before_xor1)
print(plain_text)
plain_text = rsa_decrypt(privat_key, cipher_text_before_xor2)
print(plain_text)
plain_text = rsa_decrypt(privat_key, cipher_text_before_xor3)
print(plain_text)
plain_text = rsa_decrypt(privat_key, cipher_text_before_xor4)
print(plain_text)
