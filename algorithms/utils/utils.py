import json
import pathlib


def saveKey(key: object, f_name: str, save_path: pathlib.Path, save_type: str) -> None:
    """Saves key to file.

    Parameters
    ----------
    key : object
        Key to store in file
    f_name : str
        Size of key to store whih also serves as filename
    save_path : pathlib.Path
        Path to file
    save_type : str
        Determines handling of key types for storing
    """
    if save_type == "json":
        with open(f"{save_path.joinpath(f_name)}.json", "wb+") as f_ptr:
            json.dump(key, f_ptr)

    else:
        with open(f"{save_path.joinpath(f_name)}.{save_type}", "wb+") as f_ptr:
            f_ptr.write(key)


def retrieveKey(f_name: str, save_path: pathlib.Path, save_type: str) -> object:
    """Retrieves key stored in file.

    Parameters
    ----------
    f_name : str
        Filename of key for retirieval
    save_path : pathlib.Path
        Path to file
    save_type : str
        Determines handling of key types during rerieval

    Returns
    -------
    object
        Key retrieved
    """
    if save_type == "json":
        with open(f"{save_path.joinpath(f_name)}.json", "rb+") as f_ptr:
            json.load(f_ptr)

    with open(f"{save_path.joinpath(f_name)}.{save_type}", "rb+") as f_ptr:
        key = f_ptr.read()

    return key
