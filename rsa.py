import random

# GCD based on Euclid's Algorithm


def gcd(e, r):
    while(r != 0):
        e, r = r, e % r
    return e

# Extended Euclidean Algorithm


def eea(a, b):
    if(a % b == 0):
        return(b, 0, 1)
    else:
        gcd, s, t = eea(b, a % b)
        s = s-((a//b) * t)
        return(gcd, t, s)

# Multiplicative Inverse


def mult_inv(e, r):
    gcd, s, _ = eea(e, r)
    if(gcd != 1):
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
'''DECRYPTION ALGORITHM'''


def rsa_decrypt(priv_key, c_text):
    n, d = priv_key
    txt = c_text.split(',')
    x = ''
    index = 0
    for i in txt:
        index = (int(i)**d) % n
        # print(index)
        c = chr(index)
        x += c
    return x


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
    if(gcd(i, totient) == 1):
        e_list.append(i)
e = random.choice(e_list)
e = e_list[4]
# print(e_list)
print("The value of e is: ", e)

# d value calculation
d = mult_inv(e, totient)
print("The value of d is: ", d)

privat_key = [n, d]
public_key = [n, e]

print("public and private key are: ", public_key, privat_key)
message = input("Enter Message: ")
cipher_text = rsa_encrypt(public_key, message)
print("Cipher text is : ", cipher_text)
cipher_text = input("Enter cipher text: ")
plain_text = rsa_decrypt(privat_key, cipher_text)
print(plain_text)

r = random.randint(2, n)
print(r)
txt = cipher_text.split(',')
xor_cipher_text = list()
for i in txt:
    i = int(i, base=10)
    xor_cipher_text.append(i ^ r)
print(xor_cipher_text)
