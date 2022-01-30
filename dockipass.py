#!/usr/bin/env python3


from nuclear import CliBuilder, argument, flag, parameter, subcommand
from pathlib import Path
import subprocess

DEFAULT_NAME = "dockipass"


def create_yaml(id_rsa, name=DEFAULT_NAME):
    with open("cloud-init-config/template.yaml", "r") as input_file, open(f"cloud-init-config/{name}.yaml", "w") as output_file:
        for line in input_file:
            output = line

            if (line.find("replaceme") > 0):
                output = line.replace("replaceme", id_rsa.strip())

            output_file.write(output)


def get_id_rsa():
    home = str(Path.home())
    # TODO Check if id_rsa exists
    with open(f"{home}/.ssh/id_rsa.pub") as f:
        return f.readline()


def setup():
    id_rsa = get_id_rsa()
    create_yaml(id_rsa)


def mount_users_folder(name=DEFAULT_NAME):
    cmd = f"mount /Users/ {name}"
    run_multipass(cmd)


def add_docker_context(name=DEFAULT_NAME):
    cmd = f"docker context create {name} --docker \"host=ssh://ubuntu@{name}.local\""
    run_cmd(cmd)


def remove_docker_context(name=DEFAULT_NAME):
    cmd = f"docker context rm {name}"
    run_cmd(cmd)


def use_docker_context(name=DEFAULT_NAME):
    cmd = f"docker context use {name}"
    run_cmd(cmd)


def launch(name=DEFAULT_NAME, memory="2G", disk="20G", cpu=2):
    setup()

    cmd = f"launch -c {cpu} -m {memory} -d {disk} -n {name} 20.04 --cloud-init \"cloud-init-config/{name}.yaml\""
    run_multipass(cmd)
    mount_users_folder()
    add_docker_context()
    use_docker_context()


def start(name=DEFAULT_NAME):
    cmd = f"start {name}"
    run_multipass(cmd)

def restart(name=DEFAULT_NAME):
    cmd = f"restart {name}"
    run_multipass(cmd)

def stop(name=DEFAULT_NAME):
    cmd = f"stop {name}"
    run_multipass(cmd)


def delete(name=DEFAULT_NAME):
    use_docker_context("default")
    remove_docker_context(name)
    
    cmd = f"delete {name}"
    run_multipass(cmd)
    run_multipass("purge")

def run_multipass(cmd):
    run_cmd(f"multipass {cmd.strip()}".strip())


def run_cmd(cmd):
    process = subprocess.Popen(cmd.strip(), shell=True, stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if output == b'' and process.poll() is not None:
            break
        if output:
            print(output.decode("utf-8").strip())

    rc = process.poll()


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
        ),
        subcommand("launch", help="launch multipass", run=launch).has(
            argument("name", required=False, type=str, default=DEFAULT_NAME),
            parameter("memory", "m", type=str, default="2G"),
            parameter("cpu", "c", type=int, default=2),
            parameter("disk", "d", type=str, default="20G")
        )
    ).run()


if __name__ == "__main__":
    __main__()
