
from lib.multipass import start, stop, restart, launch, launch_with_alias, delete
import unittest
from unittest.mock import patch, call
import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


@patch("lib.multipass.run_cmd")
class TestMultipass(unittest.TestCase):
    def test_start(self, mock_run_cmd):
        start("test")
        mock_run_cmd.assert_called_with("multipass start test")

    def test_restart(self, mock_run_cmd):
        restart("test")
        mock_run_cmd.assert_called_with("multipass restart test")

    def test_stop(self, mock_run_cmd):
        stop("test")
        mock_run_cmd.assert_called_with("multipass stop test")

    def test_launch(self, mock_run_cmd):
        launch("test")

        calls = [
            call("multipass launch -c 2 -m 2G -d 20G -n test 20.04 --cloud-init \"cloud-init-config/dockipass.yaml\""),
            call("multipass mount /Users/ test")
        ]

        mock_run_cmd.assert_has_calls(calls)

    def test_launch_with_alias(self, mock_run_cmd):
        launch_with_alias("test")

        calls = [
            call("multipass launch -c 2 -m 2G -d 20G -n test-alias 20.04 --cloud-init \"cloud-init-config/alias.yaml\""),
            call("multipass mount /Users/ test-alias"),
            call("multipass alias test-alias:docker docker"),
            call("multipass alias test-alias:docker-compose docker-compose")
        ]

        mock_run_cmd.assert_has_calls(calls)

    def test_delete(self, mock_run_cmd):
        delete("test")

        calls = [
            call("multipass unalias docker"),
            call("multipass unalias docker-compose"),
            call("multipass delete test-alias"),
            call("multipass purge")
        ]

        mock_run_cmd.assert_has_calls(calls)

    def test_delete_without_alias(self, mock_run_cmd):
        delete(name="test", noalias=True)

        calls = [
            call("multipass delete test"),
            call("multipass purge")
        ]

        mock_run_cmd.assert_has_calls(calls)


@patch("lib.multipass.run_cmd")
class TestLaunch(unittest.TestCase):

    def test_with_default_name(self, mock_run_cmd):
        launch()

        calls = [
            call("multipass launch -c 2 -m 2G -d 20G -n dockipass 20.04 --cloud-init \"cloud-init-config/dockipass.yaml\""),
            call("multipass mount /Users/ dockipass")
        ]

        mock_run_cmd.assert_has_calls(calls)

    def test_with_non_default_cpu(self, mock_run_cmd):
        launch(cpu=4)

        calls = [
            call("multipass launch -c 4 -m 2G -d 20G -n dockipass 20.04 --cloud-init \"cloud-init-config/dockipass.yaml\""),
            call("multipass mount /Users/ dockipass")
        ]

        mock_run_cmd.assert_has_calls(calls)

    def test_with_more_memory(self, mock_run_cmd):
        launch(memory="4G")

        calls = [
            call("multipass launch -c 2 -m 4G -d 20G -n dockipass 20.04 --cloud-init \"cloud-init-config/dockipass.yaml\""),
            call("multipass mount /Users/ dockipass")
        ]

        mock_run_cmd.assert_has_calls(calls)

    def test_with_more_disk(self, mock_run_cmd):
        launch(disk="40G")

        calls = [
            call("multipass launch -c 2 -m 2G -d 40G -n dockipass 20.04 --cloud-init \"cloud-init-config/dockipass.yaml\""),
            call("multipass mount /Users/ dockipass")
        ]

        mock_run_cmd.assert_has_calls(calls)

    def test_with_another_config(self, mock_run_cmd):
        launch(config="test")

        calls = [
            call("multipass launch -c 2 -m 2G -d 20G -n dockipass 20.04 --cloud-init \"cloud-init-config/test.yaml\""),
            call("multipass mount /Users/ dockipass")
        ]

        mock_run_cmd.assert_has_calls(calls)