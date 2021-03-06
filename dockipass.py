#!/usr/bin/env python3
__version__ = "1.0.0"

from nuclear import CliBuilder, argument, flag, parameter, subcommand
import sys

from lib.multipass import start as start_multipass, stop as stop_multipass, restart, delete as delete_multipass, launch as launch_multipass
from lib.bind_local import bind_local as _bind_local
from lib.background_task import check_for_background_task, run_task_forever, run_task_in_background, stop_task_in_background, stop_task_in_background
from lib.config import DEFAULT_NAME, HOME
from lib.status import status


def launch(name=DEFAULT_NAME, memory="2G", disk="20G", cpu=2, nobind=False):
    launched = launch_multipass(name, memory, disk, cpu)

    if (launched == False):
        print("Failed to launch Multipass")
        return

    print("Docker have now been setup and aliased")
    print(
        f"To use Docker and compose from your terminal add multipass to your path: PATH=\"{HOME}/Library/Application Support/multipass/bin\":$PATH")

    start_multipass()

    if nobind == False:
        bind_local()


def start(nobind=False):
    start_multipass()

    if nobind == False:
        bind_local()


def stop():
    stop_task_in_background("listen")
    _bind_local(cleanup=True)
    stop_multipass()


def delete():
    stop_task_in_background("listen")
    _bind_local(cleanup=True)

    delete_multipass()


def bind_local(command="start"):

    match command:
        case "start":
            started = run_task_in_background("listen")
            if started:
                print(
                    "Started to listen for portchanges in the background and binding them to localhost")
            else:
                print("Already listening for ports in background, doing nothing")
            return

        case "stop":
            stop_task_in_background("listen")
            print("Stopped listening for portchanges")

        case "cleanup":
            print("Stopped listening for portchanges and cleaned up all forwards")
            stop_task_in_background("listen")
            _bind_local(cleanup=True)


def print_status():
    print(status())


def __main__():

    if (check_for_background_task(sys.argv)):
        run_task_forever(sys.argv[2])

    CliBuilder().has(
        subcommand("start", help="start multipass", run=start).has(
            flag("nobind", "n")
        ),
        subcommand("stop", help="stop multipass", run=stop).has(),
        subcommand("restart", help="restart multipass", run=restart).has(),
        subcommand("delete", help="remove a multipass instance",
                   run=delete).has(),
        subcommand("launch", help="launch multipass", run=launch).has(
            argument("name", required=False, type=str, default=DEFAULT_NAME),
            parameter("memory", "m", type=str, default="2G"),
            parameter("cpu", "c", type=int, default=2),
            parameter("disk", "d", type=str, default="20G"),
            flag("nobind", "n")
        ),
        subcommand("listen", help="Bind forwarded docker ports to localhost", run=bind_local).has(
            argument("command", required=True, type=str,
                     strict_choices=True, choices=["start", "stop", "cleanup"]),
        ),
        subcommand("status", help="get status", run=print_status).has()
    ).run()


if __name__ == "__main__":
    __main__()
