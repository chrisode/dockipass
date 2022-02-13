#!/usr/bin/env python3

from nuclear import CliBuilder, argument, flag, parameter, subcommand
from pathlib import Path
import sys

from lib.commander import run as run_cmd
from lib.multipass import start as start_multipass, stop as stop_multipass, restart, delete as delete_multipass, launch as launch_multipass
from lib.bind_local import bind_local as _bind_local
from lib.background_task import check_for_background_task, run_task_forever, run_task_in_background, stop_task_in_background


DEFAULT_NAME = "dockipass"
HOME = str(Path.home())

def add_docker_context(name=DEFAULT_NAME):
    run_cmd(["docker", "context", "create", name, "--docker",
            f"\"host=ssh://ubuntu@{name}.local\""])


def remove_docker_context(name=DEFAULT_NAME):
    run_cmd(["docker", "context", "rm", name])


def use_docker_context(name=DEFAULT_NAME):
    run_cmd(["docker", "context", "use", name])


def launch(name=DEFAULT_NAME, memory="2G", disk="20G", cpu=2, nobind=False): 
    launch_multipass(name, memory, disk, cpu)
    print("Docker have now been setup and aliased")
    print(
        f"To use Docker and compose from your terminal add multipass to your path: \"PATH={HOME}/Library/Application Support/multipass/bin:$PATH\"")
    
    if nobind == False:
        bind_local(background=True)


def start(name=DEFAULT_NAME, nobind=False):
    start_multipass(name)

    if nobind == False:
        bind_local(background=True)


def stop(name=DEFAULT_NAME):
    stop_task_in_background("listen")
    bind_local(cleanup=True)
    stop_multipass(name)


def delete(name=DEFAULT_NAME):
    stop_task_in_background("listen")
    bind_local(cleanup=True)

    delete_multipass(name)


def bind_local(cleanup=False, verbose=False, background=False):
    if background == True:
        run_task_in_background("listen")
        print("Started to listen for portchanges in the background and binding them to localhost")
        return

    _bind_local(cleanup, verbose)


def __main__():

    if (check_for_background_task(sys.argv)):
        run_task_forever(sys.argv[2])
        return

    CliBuilder().has(
        subcommand("start", help="start multipass", run=start).has(
            argument("name", required=False, type=str, default=DEFAULT_NAME),
            flag("nobind", "n")
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
            parameter("disk", "d", type=str, default="20G"),
            flag("nobind", "n")
        ),
        subcommand("listen", help="Bind forwarded docker ports to localhost", run=bind_local).has(
            flag("cleanup", "c"),
            flag("background", "b"),
            flag("verbose", "v")
        )
    ).run()


if __name__ == "__main__":
    __main__()
