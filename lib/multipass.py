from pathlib import Path
from .commander import run as run_cmd

aliases = ["docker", "docker-compose"]

DEFAULT_NAME = "dockipass"


def start(name=DEFAULT_NAME):
    _run_multipass(["start", name])


def restart(name=DEFAULT_NAME):
    _run_multipass(["restart", name])


def stop(name=DEFAULT_NAME):
    _run_multipass(["stop", name])


def delete(name=DEFAULT_NAME, noalias=False):
    if noalias == False:
        remove_alias()
        name = f"{name}-alias"

    _run_multipass(["delete", name])
    _run_multipass(["purge"])


def launch_with_alias(name=DEFAULT_NAME, memory="2G", disk="20G", cpu=2):
    name = f"{name}-alias"
    launch(name=name, memory=memory, disk=disk, cpu=cpu, config="alias")
    create_alias(name)


def launch(name=DEFAULT_NAME, memory="2G", disk="20G", cpu=2, config=DEFAULT_NAME):
    _run_multipass(["launch", "-c", str(cpu), "-m", memory, "-d", disk, "-n",
                   name, "20.04", "--cloud-init", f"\"cloud-init-config/{config}.yaml\""], shell=True)
    mount_users_folder(name)


def remove_alias():
    for alias in aliases:
        _run_multipass(["unalias", alias])


def create_alias(name=DEFAULT_NAME):
    for alias in aliases:
        _run_multipass(["alias", f"{name}:{alias}", alias])

    modify_compose_alias()


def modify_compose_alias():
    home = str(Path.home())
    filepath = f"{home}/Library/Application Support/multipass/bin/docker-compose"

    new_file = []
    with open(filepath, "r") as file:
        output = file.read()
        for line in output.split("\n"):
            find_compose = line.find("docker-compose -- ")
            if find_compose == -1:
                new_file.append(line)
                continue

            if line.find("-f") > 0:
                return

            llenght = find_compose + len("docker-compose -- ")
            add_argument = "-f \"$(pwd)/docker-compose.yaml\" "
            line = line[:llenght] + add_argument + line[llenght:]

            new_file.append(line)

    with open(filepath, "w") as file:
        file.write("\n".join(new_file))


def mount_users_folder(name=DEFAULT_NAME):
    _run_multipass(["mount", "/Users/", name])


def _run_multipass(cmd: list, shell=False):
    cmd.insert(0, "multipass")
    run_cmd(cmd, shell=shell)
