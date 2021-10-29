from mathTools.tools import gcd, eea


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
