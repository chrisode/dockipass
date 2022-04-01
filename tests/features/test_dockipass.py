import unittest
import os
import sys
import json
from pathlib import Path

from lib.commander import find_process, kill_process
from lib.multipass import aliases, modify_compose_alias
from tests.test_helpers.common import backup_forwared, restore_forwarded
import subprocess

from sarge import run as sarge_run, Capture

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

HOME = str(Path.home())
vm_name = "feature-test"

multipass_bin_path = f"{HOME}/Library/Application Support/multipass/bin"
docker_cmd = f"{multipass_bin_path}/docker"
docker_compose_cmd = f"{multipass_bin_path}/docker-compose"


def run(cmd):
    process = sarge_run(" ".join(cmd), shell=True, stdout=Capture(), stderr=Capture())
    return process.stdout.read().decode("utf-8"), process.stderr.read().decode("utf-8")


def list_vm():
    vm, err = run(["multipass", "list", "--format", "json"])
    return json.loads(vm)

def find_vm(name):
    list = list_vm()["list"]
    for vm in list:
        if name == vm["name"]:
            return True


def vm_info():
    vm, err = run(["multipass", "info", vm_name, "--format", "json"])
    return json.loads(vm)


def kill_background_listen():
    pids = find_process("background listen")
    for pid in pids:
        kill_process(int(pid))


def restore_alias():
    name = "dockipass"
    if find_vm(name):
        for alias in aliases:
            run(["multipass", "alias", f"{name}:{alias}", alias])
        modify_compose_alias()


def remove_alias():
    name = "dockipass"
    if find_vm(name):
        for alias in aliases:
            run(["multipass", "unalias", alias])


class Feature_Test_Dockipass(unittest.TestCase):

    @classmethod
    def tearDownClass(self):
        restore_forwarded()
        kill_background_listen()
        run(["multipass", "delete", vm_name])
        run(["multipass", "purge"])
        restore_alias()

    @classmethod
    def setUpClass(self):
        backup_forwared()
        remove_alias()

    def test_1launch(self):

        launch_cmd = ["./dockipass.py", "launch", vm_name]
        run(launch_cmd)

        info = vm_info()

        self.assertEqual(len(info["errors"]), 0)
        self.assertIn(vm_name, info["info"])

        info = info["info"][vm_name]

        self.assertEqual(info["state"], "Running")
        self.assertEqual(info["image_release"], "20.04 LTS")
        self.assertIn("/Users", info["mounts"])

        # Aliases should have been setup for docker and docker-compose
        aliases = os.listdir(multipass_bin_path)
        self.assertListEqual(aliases, ["docker", "docker-compose"])

        # Docker compose alias should have file added to it
        with open(docker_compose_cmd, "r") as file:
            output = file.read()
            self.assertIn(
                '"/Library/Application Support/com.canonical.multipass/bin/multipass" docker-compose -- $arguments', output.split("\n"))

        # Check for bind
        pids = find_process("background listen")
        self.assertEqual(len(pids), 1)

    def test_1stop(self):
        run(["./dockipass.py", "stop", vm_name])

        # The containter have been stopped
        info = vm_info()["info"][vm_name]
        self.assertEqual(info["state"], "Stopped")

        # Check for bind removed
        pids = find_process("background listen")
        self.assertEqual(len(pids), 0)

    def test_2start(self):
        run(["./dockipass.py", "start", vm_name])

        # The containter is running
        info = vm_info()["info"][vm_name]
        self.assertEqual(info["state"], "Running")

        # Check for bind removed
        pids = find_process("background listen")
        self.assertEqual(len(pids), 1)

    def test_4restart(self):
        run(["./dockipass.py", "restart", vm_name])

        # The containter is running
        info = vm_info()["info"][vm_name]
        self.assertEqual(info["state"], "Running")

        # Check for bind
        pids = find_process("background listen")
        self.assertEqual(len(pids), 1)

    def test_5listen(self):
        kill_background_listen()
        pids = find_process("background listen")
        self.assertEqual(len(pids), 0)

        subprocess.run([docker_cmd, "run", "--name", "testcontainer", "-p",
                        "8081:80", "-d", "nginxdemos/hello"], stdout=subprocess.PIPE)

        subprocess.run(["./dockipass.py", "listen"])

        pids = find_process("socat")
        self.assertEqual(len(pids), 1)

        subprocess.run(["./dockipass.py", "listen", "-b"])

    def test_6dockercompose(self):
        process = subprocess.run(
            [docker_compose_cmd, "ps"], cwd=f"{parentdir}/data", stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(process.stderr.decode("utf-8"), "")
        self.assertNotEqual(process.stdout.decode("utf-8"), "")

    def test_7dockerbuildx(self):
        process = subprocess.run(
            [docker_cmd, "buildx"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        self.assertEqual(process.stderr.decode("utf-8"), "")
        self.assertIn("Usage:  docker buildx [OPTIONS] COMMAND", process.stdout.decode(
            "utf-8").split("\n"))

    def test_8delete(self):
        run(["./dockipass.py", "delete", vm_name])

        # Stopped background process
        pids = find_process("background listen")
        self.assertEqual(len(pids), 0)

        # Stopped all socat processes
        pids = find_process("socat")
        self.assertEqual(len(pids), 0)

        # VM no longer exists
        list = list_vm()["list"]
        for vm in list:
            self.assertNotIn(vm_name, vm["name"])
