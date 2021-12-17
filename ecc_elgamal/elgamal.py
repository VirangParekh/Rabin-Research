from typing import Any, Tuple

from cipher.cipher import ElGamal
from cipher.curve import Point
from cipher.key import gen_keypair


def encrypt(plain_text: str, curve: Any) -> Tuple[Tuple, Point]:
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

    return curve_pts, private_key


def decrypt(curve_pts: tuple[Point, Point], private_key: Point, curve: Any) -> str:
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


def caller(plain_text: bytes, curve: Any):
    curve_pts, private_key = encrypt(plain_text, curve)
    decrypt(curve_pts, private_key, curve)
