from platform import machine as platform_machine
from json import dumps as json_dumps, loads as json_loads
from os import path
from pathlib import Path

_config = {}
_config_path = "config/config.json"


def _reset():
    global _config
    _config = {}
    _update_config_file()


def _get_config():
    global _config
    if not _config:
        _config = _get_config_from_file()

    return _config


def _get_config_from_file():
    if not path.exists(_config_path):
        return {}

    with open(_config_path, "r") as file:
        return json_loads(file.read())


def _update_config_file():
    with open(_config_path, "w+") as file:
        file.write(json_dumps(_config))


def _update_config_key(key, value):
    global _config
    _config[key] = value
    _update_config_file()


def _get_architecture():
    machine = platform_machine()

    if not machine:
        return "amd64"

    return machine


def get_name():
    config = _get_config()
    return config.get("name")


def set_name(name):
    _update_config_key("name", name)


HOME = str(Path.home())
DEFAULT_NAME = "dockipass"
ARCHITECTURE = _get_architecture()
DOCKER_BINARY = f"{HOME}/Library/Application Support/multipass/bin/docker"
