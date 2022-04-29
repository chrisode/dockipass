from os import path
from json import loads as json_loads

_config_path = "config/config.json"
_config_content = ""


def backup_config():
    global _config_content
    if not path.exists(_config_path):
        return False

    with open(_config_path, "r") as file:
        _config_content = file.read()


def restore_config():
    if not _config_content:
        return False

    with open(_config_path, "w+") as file:
        file.write(_config_content)


def get_data(file):
    data_path = f"tests/data/{file}"

    if not path.exists(data_path):
        return

    with open(data_path, "r") as file:
        return file.read()