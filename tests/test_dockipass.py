from dockipass import launch, delete
import unittest
from unittest.mock import patch, call
import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


@patch("lib.multipass.run_cmd")
class TestLaunchDockipass(unittest.TestCase):

    @patch("builtins.print")
    def test_launch_with_alias(self, mock_print, mock_run_cmd):

        launch("test")
        calls = [
            call("multipass launch -c 2 -m 2G -d 20G -n test-alias 20.04 --cloud-init \"cloud-init-config/alias.yaml\""),
            call("multipass mount /Users/ test-alias"),
            call("multipass alias test-alias:docker docker"),
            call("multipass alias test-alias:docker-compose docker-compose")
        ]

        mock_print.assert_called()
        mock_run_cmd.assert_has_calls(calls)

    @patch("dockipass.setup")
    @patch("dockipass.run_cmd")
    def test_launch_with_noalias(self, mock_run_cmd2, mock_setup, mock_run_cmd):
        launch("test", noalias=True)

        mock_setup.assert_called_with("test")

        mock_run_cmd.assert_has_calls([
            call("multipass launch -c 2 -m 2G -d 20G -n test 20.04 --cloud-init \"cloud-init-config/test.yaml\""),
            call("multipass mount /Users/ test")
        ])

        mock_run_cmd2.assert_has_calls([
            call(
                'docker context create dockipass --docker "host=ssh://ubuntu@dockipass.local"'),
            call('docker context use dockipass')
        ])


@patch("lib.multipass.run_cmd")
class TestDeleteDockipass(unittest.TestCase):
    def test_delete_with_alias(self, mock_run_cmd):

        delete("test")

        calls = [
            call("multipass unalias docker"),
            call("multipass unalias docker-compose"),
            call("multipass delete test-alias"),
            call("multipass purge")
        ]

        mock_run_cmd.assert_has_calls(calls)

    @patch("dockipass.run_cmd")
    def test_delete_with_noalias(self, mock_run_cmd2, mock_run_cmd):

        delete("test", noalias=True)

        mock_run_cmd.assert_has_calls([
            call("multipass delete test"),
            call("multipass purge")
        ])

        mock_run_cmd2.assert_has_calls([
            call("docker context use default"),
            call("docker context rm test")
        ])
