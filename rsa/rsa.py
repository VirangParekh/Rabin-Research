from typing import Any, Tuple

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA


def keyGen(key_size: int) -> Tuple[Any, Any]:
    """Genrates key for RSA algorithm.

    Parameters
    ----------
    key_size : int
        Size of key
    """
    key_pair = RSA.generate(key_size)

    private_key = key_pair.exportKey()

    public_key = key_pair.publickey()
    public_key = public_key.exportKey()

    return private_key, public_key, key_pair


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
    private_key, public_key, key_pair = keyGen(key_size)

    key = RSA.importKey(public_key)
    encryptor = PKCS1_OAEP.new(key)
    cipher_text = encryptor.encrypt(plain_text)

    return cipher_text, private_key, key_pair


def decrypt(cipher_text: bytes, key_pair: Any) -> bytes:
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
    decryptor = PKCS1_OAEP.new(key_pair)
    plain_text = decryptor.decrypt(cipher_text)

    return plain_text


def caller(plain_text: bytes, key_size: int):
    cipher_text, private_key, key_pair = encrypt(plain_text, key_size)
    decrypt(cipher_text, key_pair)

    return plain_text, cipher_text
