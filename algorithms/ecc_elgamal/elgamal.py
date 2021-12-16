import pathlib

from utils.utils import retrieveKey, saveKey

from cipher.cipher import ElGamal
from cipher.key import gen_keypair


def keyGen(save_path: pathlib.Path, curve: str) -> None:
    """Genrates ECC key.

    Parameters
    ----------
    save_path : pathlib.Path
        Path to file
    curve: str
        ECC curve
    """
    public_key, private_key = gen_keypair(curve)

    saveKey(private_key, curve, save_path.joinpath("private"), "json")
    saveKey(public_key, curve, save_path.joinpath("public"), "json")


def encrypt(
    plain_text: str, save_path: pathlib.Path, curve: str
) -> tuple[float, float]:
    """Encrypts plain text using RSA.

    Parameters
    ----------
    plain_message : str
        Message to encrypt
    save_path : pathlib.Path
        Path to file
    curve : str
        ECC curve

    Returns
    -------
    Tuple[float, float]
        Points on elliptic curve
    """
    public_key = retrieveKey(curve, save_path.joinpath("public"), "json")

    elgamal = ElGamal(curve)
    curve_pt = elgamal.encrypt(plain_text, public_key)

    return curve_pt


def decrypt(curve_pt: tuple[float, float], save_path: pathlib.Path, curve: str) -> str:
    """Decrypts RSA encrypted text.

    Parameters
    ----------
    ciphertext : str
        Encrypted text
    save_path : pathlib.Path
        Path to file
    curve : str
        ECC curve

    Returns
    -------
    str
        Decrypted key
    """
    private_key = retrieveKey(curve, save_path.joinpath("private"), "json")

    elgamal = ElGamal(curve)
    plain_text = elgamal.decrypt(private_key, curve_pt[0], curve_pt[1])

    return plain_text
