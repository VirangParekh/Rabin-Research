from typing import Any, Tuple

import elg_cipher as ElGamal


def encrypt(plain_text: str, key_size: int) -> Tuple[Any, str]:
    """Encrypts plain text using elgamal.

    Parameters
    ----------
    plain_text : str
        Message to encrypt
    key_size : int
        Size of key

    Returns
    -------
    tuple[str, Any]
        Encrypted text
    """
    private_key, public_key = ElGamal.generate_keys(key_size).values()
    cipher_text = ElGamal.encrypt(public_key, plain_text)

    return private_key, cipher_text


def decrypt(cipher_text: str, private_key: Any) -> str:
    """Decrypts elgamal encrypted text.

    Parameters
    ----------
    cipher_text : str
        Encrypted text
    private_key : Any
        Private Key for decryption

    Returns
    -------
    str
        Decrypted text
    """
    return ElGamal.decrypt(cipher_text, private_key)


def caller(plain_text: bytes, key_size: int):
    private_key, cipher_text = encrypt(plain_text, key_size)
    decrypt(cipher_text, private_key)
