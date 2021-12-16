import pathlib

from utils.utils import retrieveKey, saveKey

from cipher.elgamal_cipher import ElGamal


def keyGen(save_path: pathlib.Path, key_size: int) -> object:
    """Genrates key for elgamal algorithm.

    Parameters
    ----------
    save_path : pathlib.Path
        Path to file
    key_size : int
        Size of key

    Returns
    -------
    object
        Elgamal object
    """
    elgamal = ElGamal()
    keyset = elgamal.generate_keys(key_size)

    saveKey(keyset, key_size, save_path.joinpath("public_private"), "json")

    return elgamal


def encrypt(
    elgamal: object, plain_message: str, save_path: pathlib.Path, key_size: int
) -> str:
    """Encrypts plain text using elgamal.

    Parameters
    ----------
    elgamal : object
        Initialized elgamal object
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
    cipher_text, session_key = elgamal.encrypt(plain_message)

    saveKey(session_key, key_size, save_path.joinpath("ephemeral"))

    return cipher_text


def decrypt(cipher_text: str, save_path: pathlib.Path, key_size: int) -> str:
    """Decrypts elgamal encrypted text.

    Parameters
    ----------
    cipher_text : str
        Encrypted text
    save_path : pathlib.Path
        Path to file
    key_size : int
        Size of key

    Returns
    -------
    str
        Decrypted text
    """
    keyset = retrieveKey(key_size, save_path.joinpath("public_private"), "json")
    session_key = retrieveKey(key_size, save_path.joinpath("public_private"), "json")

    elgamal = ElGamal(keyset)
    plain_text = elgamal.decrypt([cipher_text, session_key])

    return plain_text
