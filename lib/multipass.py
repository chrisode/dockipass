from .config import DEFAULT_NAME, ARCHITECTURE, get_name as get_name_from_config, set_name, _reset
from .commander import run as run_cmd
from .docker import patch_compose
import json


_aliases = ["docker", "docker-compose"]


def get_name():
    name = get_name_from_config()

    if not name:
        return DEFAULT_NAME

    return name


def start():
    _run_multipass(["start", get_name()])


def restart():
    _run_multipass(["restart", get_name()])


def stop():
    _run_multipass(["stop", get_name()])


def delete():
    remove_alias()
    _run_multipass(["delete",  get_name()])
    _run_multipass(["purge"])
    _reset()


def get_info():
    info, status = _run_multipass(
        ["info", get_name(), "--format", "json"], live=False)

    if status == False:
        not_exists = info.find("does not exist") > -1

        if not_exists == True:
            print("The instance doesnt exist")
        else:
            print(info)

        return False

    return json.loads(info)


def check_aliases():
    name = get_name()
    aliases = get_aliases()

    if not aliases:
        return False

    only_aliases = []
    for alias in aliases:
        if alias.get("alias") in _aliases and alias.get("instance") != name:
            return False

        only_aliases.append(alias.get("alias"))
    
    
    for _alias in _aliases:
        if _alias not in only_aliases:
            return False

    return True

def get_aliases():
    aliases, status = _run_multipass(
        ["aliases", "--format", "json"], live=False)

    if status == False:
        return []

    return json.loads(aliases).get("aliases")


def launch(name=DEFAULT_NAME, memory="2G", disk="20G", cpu=2):
    if get_name_from_config():
        return False

    launched = _run_multipass(["launch", "-c", str(cpu), "-m", memory, "-d", disk, "-n",
                              name, "20.04", "--cloud-init", f"\"cloud-init-config/{ARCHITECTURE}.yaml\""], shell=True)

    if launched == False:
        return False

    set_name(name)

    mount_users_folder(name)
    create_alias(name)


def remove_alias():
    for alias in _aliases:
        _run_multipass(["unalias", alias])


def create_alias(name):
    for alias in _aliases:
        _run_multipass(["alias", f"{name}:{alias}", alias])

    patch_compose()


def mount_users_folder(name=DEFAULT_NAME):
    _run_multipass(["mount", "/Users/", name])


def _run_multipass(cmd: list, shell=False, live=True):
    cmd.insert(0, "multipass")
    return run_cmd(cmd, shell=shell, live=live)
