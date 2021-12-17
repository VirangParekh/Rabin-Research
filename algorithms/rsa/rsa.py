from typing import Any, Tuple

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import rsa as RSA
from cryptography.hazmat.primitives.asymmetric.padding import MGF1, OAEP


def keyGen(key_size: int) -> Tuple[Any, Any]:
    """Genrates key for RSA algorithm.

    Parameters
    ----------
    key_size : int
        Size of key
    """
    private_key = RSA.generate_private_key(65537, key_size)
    public_key = private_key.public_key()

    return private_key, public_key


def encrypt(plain_text: bytes, key_size: int) -> Tuple[bytes, Any]:
    """Encrypts plain text using RSA.

    Parameters
    ----------
    plain_message : bytes
        Message to encrypt
    key_size : int
        Size of key

    Returns
    -------
    Tuple[bytes, Any]
        Private Key, Encrypted text
    """
    private_key, public_key = keyGen(key_size)

    cipher_text = public_key.encrypt(
        plain_text,
        OAEP(MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None),
    )

    return cipher_text, private_key


def decrypt(cipher_text: bytes, private_key: Any) -> bytes:
    """Decrypts RSA encrypted text.

    Parameters
    ----------
    ciphertext : bytes
        Encrypted text
    key_size : Any
        Size of key

    Returns
    -------
    bytes
        Decrypted text
    """
    plain_text = private_key.decrypt(
        cipher_text,
        OAEP(
            mgf=MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None
        ),
    )

    return plain_text
