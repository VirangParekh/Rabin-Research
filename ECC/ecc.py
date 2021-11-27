from ecc.curve import Curve25519
from ecc.key import gen_keypair
from ecc.cipher import ElGamal

plain_text = b"Paper khatam karo"

pvt, pub = gen_keypair(Curve25519)

cipher_elg = ElGamal(Curve25519)

C1, C2 = cipher_elg.encrypt(plain_text, pub)
# Decrypt
new_plaintext = cipher_elg.decrypt(pvt, C1, C2)

print(new_plaintext == plain_text)
