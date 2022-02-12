import unittest
from unittest.mock import patch, call
import os
import sys
import json
from pathlib import Path
from lib.commander import run, find_process, kill_process
from lib.multipass import aliases
from tests.test_helpers.common import backup_forwared, restore_forwarded

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

HOME = str(Path.home())
vm_name = "feature-test"
vm_name_alias = f"{vm_name}-alias"


def list_vm():
    vm = run(["multipass", "list", "--format", "json"], live=False, shell=True)
    return json.loads(vm)


def find_vm(name):
    list = list_vm()["list"]
    for vm in list:
        if name == vm["name"]:
            return True


def vm_info():
    vm = run(["multipass", "info", vm_name_alias,
             "--format", "json"], live=False, shell=True)
    return json.loads(vm)


def kill_background_listen():
    pids = find_process("background listen")
    for pid in pids:
        kill_process(int(pid))


def restore_alias():
    name = "dockipass-alias"
    if find_vm(name):
        for alias in aliases:
            run(["multipass", "alias",
                f"{name}:{alias}", alias], live=False, mute_error=True)


def remove_alias():
    name = "dockipass-alias"
    if find_vm(name):
        for alias in aliases:
            run(["multipass", "unalias", alias])


class Feature_Test_Dockipass(unittest.TestCase):

    # Setup and teardown that handles preserving current state
    @classmethod
    def tearDownClass(self):
        restore_forwarded()
        kill_background_listen()
        run(["multipass", "delete",
            f"{vm_name}-alias"], live=False, mute_error=True)
        run(["multipass", "purge"], live=False, mute_error=True)
        restore_alias()

    @classmethod
    def setUpClass(self):
        backup_forwared()
        remove_alias()

    # def test_fun_test(self):
    #     with open("forwared_ports.json", "w+") as file:
    #         file.write("{}")

    def test_1launch(self):

        launch_cmd = ["./dockipass.py", "launch", vm_name]
        run(launch_cmd, shell=True, live=False)

        info = vm_info()

        self.assertEqual(len(info["errors"]), 0)
        self.assertIn(vm_name_alias, info["info"])

        info = info["info"][vm_name_alias]

        self.assertEqual(info["state"], "Running")
        self.assertEqual(info["image_release"], "20.04 LTS")
        self.assertIn("/Users", info["mounts"])

        # Aliases should have been setup for docker and docker-compose
        aliases = os.listdir(f"{HOME}/Library/Application Support/multipass/bin")
        self.assertListEqual(aliases, ["docker", "docker-compose"])

        # Check for bind
        pids = find_process("background listen")
        self.assertEqual(len(pids), 1)

    def test_1stop(self):
        run(["./dockipass.py", "stop", vm_name_alias], shell=True, live=False)

        # The containter have been stopped
        info = vm_info()["info"][vm_name_alias]
        self.assertEqual(info["state"], "Stopped")

        # Check for bind removed
        pids = find_process("background listen")
        self.assertEqual(len(pids), 0)

    def test_2start(self):
        run(["./dockipass.py", "start", vm_name_alias], shell=False, live=False)

        # The containter is running
        info = vm_info()["info"][vm_name_alias]
        self.assertEqual(info["state"], "Running")

        # Check for bind removed
        pids = find_process("background listen")
        self.assertEqual(len(pids), 1)

    def test_4restart(self):
        run(["./dockipass.py", "restart", vm_name_alias], shell=True, live=False)

        # The containter is running
        info = vm_info()["info"][vm_name_alias]
        self.assertEqual(info["state"], "Running")

        # Check for bind
        pids = find_process("background listen")
        self.assertEqual(len(pids), 1)

    def test_5listen(self):
        kill_background_listen()
        pids = find_process("background listen")
        self.assertEqual(len(pids), 0)

        run(["docker", "run", "--name", "testcontainer", "-p", "8081:80", "-d", "nginxdemos/hello"], shell=True, live=False, mute_error=True)
        run(["./dockipass.py", "listen"], shell=True, live=False)

        pids = find_process("socat")
        self.assertEqual(len(pids), 1)

        run(["./dockipass.py", "listen", "-b"], shell=True, live=False)

    def test_6delete(self):
        run(["./dockipass.py", "delete", vm_name], shell=True, live=False)

        # Stopped background process
        pids = find_process("background listen")
        self.assertEqual(len(pids), 0)

        # Stopped all socat processes
        pids = find_process("socat")
        self.assertEqual(len(pids), 0)

        # VM no longer exists
        list = list_vm()["list"]
        for vm in list:
            self.assertNotIn(vm_name_alias, vm["name"])
