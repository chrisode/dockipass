from dockipass import launch, start, delete, bind_local, stop
import unittest
from unittest.mock import patch, call, Mock
import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


@patch("lib.config._config.config", {})
@patch("lib.config._config.update_config_file", Mock())
@patch("lib.multipass.run_cmd", return_value=True)
class TestDockipass(unittest.TestCase):

    @patch("builtins.print")
    @patch("dockipass.bind_local")
    @patch("lib.multipass.patch_compose")
    @patch("lib.multipass.ARCHITECTURE", "amd64")
    def test_launch(self, mock_alias_compose, mock_bind_local, mock_print, mock_run_cmd):

        launch("test")
        calls = [
            call(["multipass", "launch", "-c", "2", "-m", "2G", "-d", "20G", "-n", "test",
                 "20.04", "--cloud-init", f"\"cloud-init-config/amd64.yaml\""], shell=True, live=True),
            call(["multipass", "mount", "/Users/", "test"], shell=False, live=True),
            call(["multipass", "alias", "test:docker", "docker"], shell=False, live=True),
            call(["multipass", "alias", "test:docker-compose",
                 "docker-compose"], shell=False, live=True)
        ]

        mock_print.assert_called()
        mock_run_cmd.assert_has_calls(calls)

        mock_bind_local.assert_called()

    @patch("dockipass.bind_local")
    @patch("dockipass.start_multipass")
    def test_start(self, mock_start, mock_bind_local, mock_run_cmd):
        start()
        mock_start.assert_called()

        mock_bind_local.assert_called()

    @patch("dockipass.bind_local")
    @patch("dockipass.start_multipass")
    def test_start_and_not_binding_ports(self, mock_start, mock_bind_local, mock_run_cmd):
        start(nobind=True)

        mock_start.assert_called()

        mock_bind_local.assert_not_called()

    @patch("dockipass._bind_local")
    @patch("dockipass.stop_task_in_background")
    @patch("dockipass.stop_multipass")
    def test_stop(self, mock_stop, mock_stop_task, mock_bind_local, mock_run_cmd):
        stop()
        mock_stop.assert_called()

        mock_stop_task.assert_called_with("listen")
        mock_bind_local.assert_called_with(cleanup=True)

    def test_delete(self, mock_run_cmd):

        delete()

        calls = [
            call(["multipass", "unalias", "docker"], shell=False, live=True),
            call(["multipass", "unalias", "docker-compose"], shell=False, live=True),
            call(["multipass", "delete", "dockipass"], shell=False, live=True),
            call(["multipass", "purge"], shell=False, live=True)
        ]

        mock_run_cmd.assert_has_calls(calls)

    @patch("builtins.print")
    @patch("dockipass.run_task_in_background")
    def test_bind_local_in_background(self, mock_run_task_in_background, mock_print, mock_run_cmd):
        bind_local(command="start")
        mock_run_task_in_background.assert_called_with("listen")
        mock_print.assert_called_with(
            "Started to listen for portchanges in the background and binding them to localhost")

    @patch("builtins.print")
    @patch("dockipass.stop_task_in_background")
    def test_bind_local_in_background(self, mock_stop_task_in_background, mock_print, mock_run_cmd):
        bind_local(command="stop")
        mock_stop_task_in_background.assert_called_with("listen")
        mock_print.assert_called_with("Stopped listening for portchanges")

    @patch("builtins.print")
    @patch("dockipass.stop_task_in_background")
    @patch("dockipass._bind_local")
    def test_bind_local_in_background(self, mock_bind_local, mock_stop_task_in_background, mock_print, mock_run_cmd):
        bind_local(command="cleanup")
        mock_stop_task_in_background.assert_called_with("listen")
        mock_bind_local.assert_called_with(cleanup=True)
        mock_print.assert_called_with(
            "Stopped listening for portchanges and cleaned up all forwards")
