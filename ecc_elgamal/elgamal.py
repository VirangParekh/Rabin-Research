from typing import Any, Tuple

from cipher.cipher import ElGamal
from cipher.curve import Point
from cipher.key import gen_keypair


def encrypt(plain_text: str, curve: Any) -> Tuple[Any, str, Point]:
    """Encrypts plain text using RSA.

    Parameters
    ----------
    plain_message : str
        Message to encrypt
    curve : Any
        ECC curve

    Returns
    -------
    Tuple[tuple, Point]
        Points on elliptic curve
    """
    private_key, public_key = gen_keypair(curve)

    elgamal = ElGamal(curve)
    curve_pts = elgamal.encrypt(plain_text, public_key)

    return private_key, plain_text, curve_pts


def decrypt(curve_pts: Tuple[Point, Point],
            private_key: Point,
            curve: Any) -> str:
    """Decrypts RSA encrypted text.

    Parameters
    ----------
    curve_pts : tuple[Point, Point]
        ECC points on curve
    private_key : Point
        Private Key for decryption
    curve : Any
        ECC curve

    Returns
    -------
    str
        Decrypted key
    """
    elgamal = ElGamal(curve)
    plain_text = elgamal.decrypt(private_key, curve_pts[0], curve_pts[1])

    return plain_text
