from dockipass import launch, start, delete, bind_local, stop
import unittest
from unittest.mock import patch, call
import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


@patch("lib.multipass.run_cmd")
class TestDockipass(unittest.TestCase):

    @patch("builtins.print")
    @patch("dockipass.bind_local")
    def test_launch_with_alias(self, mock_bind_local, mock_print, mock_run_cmd):

        launch("test")
        calls = [
            call(["multipass", "launch", "-c", "2", "-m", "2G", "-d", "20G", "-n", "test",
                 "20.04", "--cloud-init", f"\"cloud-init-config/alias.yaml\""], shell=True),
            call(["multipass", "mount", "/Users/", "test"], shell=False),
            call(["multipass", "alias", "test:docker", "docker"], shell=False),
            call(["multipass", "alias", "test:docker-compose",
                 "docker-compose"], shell=False)
        ]

        mock_print.assert_called()
        mock_run_cmd.assert_has_calls(calls)

        mock_bind_local.assert_called_with(background=True)

    @patch("dockipass.bind_local")
    @patch("dockipass.start_multipass")
    def test_start(self, mock_start, mock_bind_local, mock_run_cmd):
        start("test")
        mock_start.assert_called_with("test")

        mock_bind_local.assert_called_with(background=True)

    @patch("dockipass.bind_local")
    @patch("dockipass.start_multipass")
    def test_start_and_not_binding_ports(self, mock_start, mock_bind_local, mock_run_cmd):
        start("test", nobind=True)

        mock_start.assert_called_with("test")

        mock_bind_local.assert_not_called()

    @patch("dockipass.bind_local")
    @patch("dockipass.stop_task_in_background")
    @patch("dockipass.stop_multipass")
    def test_stop(self, mock_stop, mock_stop_task, mock_bind_local, mock_run_cmd):
        stop("test")
        mock_stop.assert_called_with("test")

        mock_stop_task.assert_called_with("listen")
        mock_bind_local.assert_called_with(cleanup=True)

    def test_delete(self, mock_run_cmd):

        delete("test")

        calls = [
            call(["multipass", "unalias", "docker"], shell=False),
            call(["multipass", "unalias", "docker-compose"], shell=False),
            call(["multipass", "delete", "test"], shell=False),
            call(["multipass", "purge"], shell=False)
        ]

        mock_run_cmd.assert_has_calls(calls)

    @patch("builtins.print")
    @patch("dockipass.run_task_in_background")
    def test_bind_local_in_background(self, mock_run_task_in_background, mock_print, mock_run_cmd):
        bind_local(background=True)
        mock_run_task_in_background.assert_called_with("listen")
        mock_print.assert_called_with(
            "Started to listen for portchanges in the background and binding them to localhost")
