import pathlib

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from utils.utils import retrieveKey, saveKey


def keyGen(save_path: pathlib.Path, key_size: int) -> None:
    """Genrates key for RSA algorithm.

    Parameters
    ----------
    save_path : pathlib.Path
        Path to file
    key_size : int
        Size of key
    """
    key = RSA.generate(key_size)

    private_key = key.export_key()
    saveKey(private_key, key_size, save_path.joinpath("private"), "pem")

    public_key = key.publickey().export_key()
    saveKey(public_key, key_size, save_path.joinpath("public"), "pem")


def encrypt(plain_text: str, save_path: pathlib.Path, key_size: int) -> str:
    """Encrypts plain text using RSA.

    Parameters
    ----------
    plain_message : str
        Message to encrypt
    save_path : pathlib.Path
        Path to file
    key_size : int
        Size of key

    Returns
    -------
    str
        Encrypted text
    """
    public_key = RSA.import_key(
        retrieveKey(key_size, save_path.joinpath("public"), "pem")
    )

    rsa_encryptor = PKCS1_OAEP.new(public_key)
    cipher_text = rsa_encryptor.encrypt(plain_text)

    return cipher_text


def decrypt(cipher_text: str, save_path: pathlib.Path, key_size: int) -> str:
    """Decrypts RSA encrypted text.

    Parameters
    ----------
    ciphertext : str
        Encrypted text
    save_path : pathlib.Path
        Path to file
    key_size : int
        Size of key

    Returns
    -------
    str
        Decrypted key
    """
    private_key = RSA.import_key(
        retrieveKey(key_size, save_path.joinpath("private"), "pem")
    )

    rsa_decryptor = PKCS1_OAEP.new(private_key)
    plain_text = rsa_decryptor.decrypt(cipher_text)

    return plain_text
