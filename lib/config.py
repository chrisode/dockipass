from ast import ClassDef
from platform import machine as platform_machine
from json import dumps as json_dumps, loads as json_loads
from os import path
from pathlib import Path

class Config:

    config_path = "config/config.json"

    def __init__(self):
        self.config = {}
        self.update_config_from_file()

    def reset(self):
        self.config = {}
        self.update_config_file()

    def update_config_from_file(self):
        if not path.exists(self.config_path):
            return

        with open(self.config_path, "r") as file:
            self.config = json_loads(file.read())


    def update_config_file(self):
        with open(self.config_path, "w+") as file:
            file.write(json_dumps(self.config))

    def get(self, key):
        return self.config.get(key)

    def set(self, key, value):
        self.config[key] = value
        self.update_config_file()


_config = Config() 

def _reset():
   _config.reset()


def _get_architecture():
    machine = platform_machine()

    if not machine:
        return "amd64"

    return machine


def get_name():
    return _config.get("name")


def set_name(name):
    _config.set("name", name)


def get_forwarded_ports():
    ports = _config.get("forwarded_ports")
    if not ports:
        return {}
    return ports


def set_forwarded_ports(ports):
    _config.set("forwarded_ports", ports)


HOME = str(Path.home())
DEFAULT_NAME = "dockipass"
ARCHITECTURE = _get_architecture()
DOCKER_BINARY = f"{HOME}/Library/Application Support/multipass/bin/docker"
