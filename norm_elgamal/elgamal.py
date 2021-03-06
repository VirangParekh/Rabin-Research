from typing import Any, Tuple

import elg_cipher as ElGamal


def encrypt(plain_text: str, key_size: int) -> Tuple[Any, str, str]:
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
    private_key, public_key = ElGamal.generate_keys(iNumBits=key_size).values()
    cipher_text = ElGamal.encrypt(public_key, plain_text)

    return private_key, plain_text, cipher_text


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
