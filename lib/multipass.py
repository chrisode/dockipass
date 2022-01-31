from os import remove
from .commander import run as run_cmd

aliases = ["docker", "docker-compose"]

DEFAULT_NAME = "dockipass"


def start(name=DEFAULT_NAME):
    cmd = f"start {name}"
    _run_multipass(cmd)


def restart(name=DEFAULT_NAME):
    cmd = f"restart {name}"
    _run_multipass(cmd)


def stop(name=DEFAULT_NAME):
    cmd = f"stop {name}"
    _run_multipass(cmd)


def delete(name=DEFAULT_NAME, noalias=False):
    if noalias == False:
        remove_alias()
        name = f"{name}-alias"

    _run_multipass(f"delete {name}")
    _run_multipass("purge")


def launch_with_alias(name=DEFAULT_NAME, memory="2G", disk="20G", cpu=2):
    name = f"{name}-alias"
    launch(name=name, memory=memory, disk=disk, cpu=cpu, config="alias")
    create_alias(name)


def launch(name=DEFAULT_NAME, memory="2G", disk="20G", cpu=2, config=DEFAULT_NAME):
    cmd = f"launch -c {cpu} -m {memory} -d {disk} -n {name} 20.04 --cloud-init \"cloud-init-config/{config}.yaml\""
    _run_multipass(cmd)
    mount_users_folder(name)


def remove_alias():
    for alias in aliases:
        _run_multipass(f"unalias {alias}")


def create_alias(name=DEFAULT_NAME):
    for alias in aliases:
        _run_multipass(f"alias {name}:{alias} {alias}")


def mount_users_folder(name=DEFAULT_NAME):
    cmd = f"mount /Users/ {name}"
    _run_multipass(cmd)


def _run_multipass(cmd):
    run_cmd(f"multipass {cmd.strip()}".strip())
