#!/usr/bin/env python3

from nuclear import CliBuilder, argument, flag, parameter, subcommand
from pathlib import Path

from lib.commander import run as run_cmd
from lib.multipass import launch_with_alias, start, stop, restart, delete as delete_multipass, launch as launch_multipass

DEFAULT_NAME = "dockipass"
HOME = str(Path.home())


def create_yaml(id_rsa, name=DEFAULT_NAME):
    with open("cloud-init-config/template.yaml", "r") as input_file, open(f"cloud-init-config/{name}.yaml", "w") as output_file:
        for line in input_file:
            output = line

            if (line.find("replaceme") > 0):
                output = line.replace("replaceme", id_rsa.strip())

            output_file.write(output)


def get_id_rsa():
    # TODO Check if id_rsa exists
    with open(f"{HOME}/.ssh/id_rsa.pub") as f:
        return f.readline()


def setup():
    id_rsa = get_id_rsa()
    create_yaml(id_rsa)


def add_docker_context(name=DEFAULT_NAME):
    cmd = f"docker context create {name} --docker \"host=ssh://ubuntu@{name}.local\""
    run_cmd(cmd)


def remove_docker_context(name=DEFAULT_NAME):
    cmd = f"docker context rm {name}"
    run_cmd(cmd)


def use_docker_context(name=DEFAULT_NAME):
    cmd = f"docker context use {name}"
    run_cmd(cmd)


def launch(name=DEFAULT_NAME, memory="2G", disk="20G", cpu=2, noalias=False):

    if noalias == False:
        launch_with_alias(name, memory, disk, cpu)
        print("Docker have now been setup and aliased")
        print(
            f"To use Docker and compose from your terminal add multipass to your path: \"PATH={HOME}/Library/Application Support/multipass/bin:$PATH\"")
        return

    setup()

    launch_multipass(name, memory, disk, cpu, name)

    add_docker_context()
    use_docker_context()


def delete(name=DEFAULT_NAME, noalias=False):
    if noalias == True:
        use_docker_context("default")
        remove_docker_context(name)

    delete_multipass(name, noalias)


def __main__():
    CliBuilder().has(
        subcommand("start", help="start multipass", run=start).has(
            argument("name", required=False, type=str, default=DEFAULT_NAME),
        ),
        subcommand("stop", help="stop multipass", run=stop).has(
            argument("name", required=False, type=str, default=DEFAULT_NAME),
        ),
        subcommand("restart", help="restart multipass", run=restart).has(
            argument("name", required=False, type=str, default=DEFAULT_NAME),
        ),
        subcommand("delete", help="remove a multipass instance", run=delete).has(
            argument("name", required=False, type=str, default=DEFAULT_NAME),
            flag("noalias")
        ),
        subcommand("launch", help="launch multipass", run=launch).has(
            argument("name", required=False, type=str, default=DEFAULT_NAME),
            parameter("memory", "m", type=str, default="2G"),
            parameter("cpu", "c", type=int, default=2),
            parameter("disk", "d", type=str, default="20G"),
            flag("noalias", "n")
        )
    ).run()


if __name__ == "__main__":
    __main__()
