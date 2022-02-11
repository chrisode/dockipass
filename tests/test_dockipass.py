from dockipass import launch, start, delete, bind_local
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
    @patch("dockipass.bind_local")
    def test_launch_with_alias(self, mock_bind_local, mock_print, mock_run_cmd):

        launch("test")
        calls = [
            call(["multipass", "launch", "-c", "2", "-m", "2G", "-d", "20G", "-n", "test-alias",
                 "20.04", "--cloud-init", f"\"cloud-init-config/alias.yaml\""], shell=True),
            call(["multipass", "mount", "/Users/", "test-alias"], shell=False),
            call(["multipass", "alias", "test-alias:docker", "docker"], shell=False),
            call(["multipass", "alias", "test-alias:docker-compose",
                 "docker-compose"], shell=False)
        ]

        mock_print.assert_called()
        mock_run_cmd.assert_has_calls(calls)

        mock_bind_local.assert_called_with(background=True)

    @patch("dockipass.setup")
    @patch("dockipass.run_cmd")
    @patch("dockipass.bind_local")
    def test_launch_with_noalias(self, mock_bind_local, mock_run_cmd2, mock_setup, mock_run_cmd):
        launch("test", noalias=True)

        mock_setup.assert_called_with("test")

        mock_run_cmd.assert_has_calls([
            call(["multipass", "launch", "-c", "2", "-m", "2G", "-d", "20G", "-n", "test",
                 "20.04", "--cloud-init", f"\"cloud-init-config/test.yaml\""], shell=True),
            call(["multipass", "mount", "/Users/", "test"], shell=False),
        ])

        mock_run_cmd2.assert_has_calls([
            call(
                ["docker", "context", "create", "dockipass", "--docker", "\"host=ssh://ubuntu@dockipass.local\""]),
            call(["docker", "context", "use", "dockipass"])
        ])

        mock_bind_local.assert_called_with(background=True)

    @patch("dockipass.bind_local")
    @patch("dockipass.start_multipass")
    def test_start(self, mock_start, mock_bind_local, mock_run_cmd):
        start("test")
        mock_start.assert_called_with("test")

        mock_bind_local.assert_called_with(background=True)

    @patch("builtins.print")
    @patch("dockipass.bind_local")
    @patch("dockipass.start_multipass")
    def test_start_and_not_binding_ports(self, mock_start, mock_bind_local, mock_print, mock_run_cmd):
        start("test", nobind=True)

        mock_start.assert_called_with("test")

        mock_bind_local.assert_not_called()

        mock_print.assert_not_called()


@patch("lib.multipass.run_cmd")
class TestDeleteDockipass(unittest.TestCase):
    def test_delete_with_alias(self, mock_run_cmd):

        delete("test")

        calls = [
            call(["multipass", "unalias", "docker"], shell=False),
            call(["multipass", "unalias", "docker-compose"], shell=False),
            call(["multipass", "delete", "test-alias"], shell=False),
            call(["multipass", "purge"], shell=False)
        ]

        mock_run_cmd.assert_has_calls(calls)

    @patch("dockipass.run_cmd")
    def test_delete_with_noalias(self, mock_run_cmd2, mock_run_cmd):

        delete("test", noalias=True)

        mock_run_cmd.assert_has_calls([
            call(["multipass", "delete", "test"], shell=False),
            call(["multipass", "purge"], shell=False)
        ])

        mock_run_cmd2.assert_has_calls([
            call(["docker", "context", "use", "default"]),
            call(["docker", "context", "rm", "test"])
        ])


class TestDockipass(unittest.TestCase):
    @patch("builtins.print")
    @patch("dockipass.run_task_in_background")
    def test_bind_local_in_background(self, mock_run_task_in_background, mock_print):
        bind_local(background=True)
        mock_run_task_in_background.assert_called_with("listen")
        mock_print.assert_called_with("Started to listen for portchanges in the background and binding them to localhost")
