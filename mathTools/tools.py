def gcd(e, r):
    while r != 0:
        e, r = r, e % r
    return e


def eea(a, b):
    if a % b == 0:
        return (b, 0, 1)
    else:
        gcd, s, t = eea(b, a % b)
        s = s - ((a // b) * t)
        return (gcd, t, s)


def mult_inv(e, r):
    gcd, s, _ = eea(e, r)
    if gcd != 1:
        return None
    else:
        return s % r
