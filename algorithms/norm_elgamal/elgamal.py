from typing import Any, Tuple

import cipher.elg_cipher as ElGamal


def encrypt(key_size: int, plain_text: str) -> Tuple[Any, str]:
    """Encrypts plain text using elgamal.

    Parameters
    ----------
    key_size : int
        Size of key
    plain_text : str
        Message to encrypt

    Returns
    -------
    tuple[str, Any]
        Encrypted text
    """
    private_key, public_key = ElGamal.generate_keys(key_size).values()
    cipher_text = ElGamal.encrypt(public_key, plain_text)

    return private_key, cipher_text


def decrypt(private_key: Any, cipher_text: str) -> str:
    """Decrypts elgamal encrypted text.

    Parameters
    ----------
    private_key : Any
        Private Key for decryption
    cipher_text : str
        Encrypted text

    Returns
    -------
    str
        Decrypted text
    """
    return ElGamal.decrypt(private_key, cipher_text)


if __name__ == "__main__":
    private_key, cipher_text = encrypt(128, "Hello I am Amogh")
    decrypt(private_key, cipher_text)
