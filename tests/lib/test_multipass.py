
from lib.multipass import start, stop, restart, launch, delete, set_name
import unittest
from unittest.mock import patch, call, mock_open, Mock
import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


@patch("lib.multipass.run_cmd", return_value=True)
@patch("lib.config._get_config_from_file", Mock(return_value={}))
@patch("lib.config._update_config_file", Mock())
class TestMultipass(unittest.TestCase):

    @patch("lib.config._update_config_file", Mock())
    def setUp(self):
        set_name(None)

    @patch("lib.config._update_config_file", Mock())
    def tearDown(self):
        set_name(None)

    def test_start(self, mock_run_cmd):
        set_name("test")
        start()
        mock_run_cmd.assert_called_with(
            ["multipass", "start", "test"], shell=False)

    def test_restart(self, mock_run_cmd):
        set_name("test")
        restart()
        mock_run_cmd.assert_called_with(
            ["multipass", "restart", "test"], shell=False)

    def test_stop(self, mock_run_cmd):
        set_name("test")
        stop()
        mock_run_cmd.assert_called_with(
            ["multipass", "stop", "test"], shell=False)

    @patch("builtins.open", new_callable=mock_open, read_data="#!/bin/sh\n\ndocker-compose -- awd")
    @patch("lib.multipass.ARCHITECTURE", "amd64")
    def test_launch(self, mock_mock_open, mock_run_cmd):
        launch("test")

        calls = [
            call(["multipass", "launch", "-c", "2", "-m", "2G", "-d", "20G", "-n",
                 "test", "20.04", "--cloud-init", f"\"cloud-init-config/amd64.yaml\""], shell=True),
            call(["multipass", "mount", "/Users/", "test"], shell=False),
            call(["multipass", "alias", "test:docker", "docker"], shell=False),
            call(["multipass", "alias", "test:docker-compose",
                 "docker-compose"], shell=False)
        ]

        mock_run_cmd.assert_has_calls(calls)
        mock_file = mock_mock_open()
        mock_mock_open.assert_called()
        mock_file.read.assert_called()
        mock_file.write.assert_called_once_with(
            '#!/bin/sh\n\narguments=""\nf_arg=""\n\nfor (( i=1; i <= "$#"; i++ )); do\n    arg=${!i}\n    arguments+=" $arg"\n    if [[ $arg = "-f" ]]; then\n        i=$((i+1))\n        f_arg=${!i}\n        if [[ "$f_arg" == *"/Users"* ]]; then\n            arguments+=" $f_arg"\n        else\n            arguments+=" $(pwd)/$f_arg"\n        fi\n    fi    \ndone\n\nif [[ -z $f_arg ]]; then\n    f_arg="$(pwd)/docker-compose.yml"\n    if [[ -f $f_arg ]]; then\n        arguments="-f "$f_arg$arguments\n    else\n        arguments="-f $(pwd)/docker-compose.yaml"$arguments\n    fi\nfi\n    \n\ndocker-compose -- $arguments')

    def test_delete(self, mock_run_cmd):
        set_name("test")
        delete()

        calls = [
            call(["multipass", "unalias", "docker"], shell=False),
            call(["multipass", "unalias", "docker-compose"], shell=False),
            call(["multipass", "delete", "test"], shell=False),
            call(["multipass", "purge"], shell=False),
        ]

        mock_run_cmd.assert_has_calls(calls)


@patch("lib.multipass.ARCHITECTURE", "amd64")
@patch("builtins.open", new_callable=mock_open)
@patch("lib.multipass.run_cmd", return_value=True)
@patch("lib.config._get_config_from_file", Mock(return_value={}))
@patch("lib.config._update_config_file", Mock())
class TestLaunch(unittest.TestCase):

    @patch("lib.config._update_config_file", Mock())
    def setUp(self):
        set_name(None)

    @patch("lib.config._update_config_file", Mock())
    def tearDown(self):
        set_name(None)

    def test_with_default_name(self, mock_run_cmd, mopen):
        launch()

        calls = [
            call(["multipass", "launch", "-c", "2", "-m", "2G", "-d", "20G", "-n",
                 "dockipass", "20.04", "--cloud-init", f"\"cloud-init-config/amd64.yaml\""], shell=True),
            call(["multipass", "mount", "/Users/", "dockipass"], shell=False),
            call(["multipass", "alias", "dockipass:docker", "docker"], shell=False),
            call(["multipass", "alias", "dockipass:docker-compose",
                 "docker-compose"], shell=False)
        ]

        mock_run_cmd.assert_has_calls(calls)

    def test_with_non_default_cpu(self, mock_run_cmd, mopen):
        launch(cpu=4)

        calls = [
            call(["multipass", "launch", "-c", "4", "-m", "2G", "-d", "20G", "-n",
                 "dockipass", "20.04", "--cloud-init", f"\"cloud-init-config/amd64.yaml\""], shell=True),
            call(["multipass", "mount", "/Users/", "dockipass"], shell=False),
            call(["multipass", "alias", "dockipass:docker", "docker"], shell=False),
            call(["multipass", "alias", "dockipass:docker-compose",
                 "docker-compose"], shell=False)
        ]

        mock_run_cmd.assert_has_calls(calls)

    def test_with_more_memory(self, mock_run_cmd, mopen):
        launch(memory="4G")

        calls = [
            call(["multipass", "launch", "-c", "2", "-m", "4G", "-d", "20G", "-n",
                 "dockipass", "20.04", "--cloud-init", f"\"cloud-init-config/amd64.yaml\""], shell=True),
            call(["multipass", "mount", "/Users/", "dockipass"], shell=False),
            call(["multipass", "alias", "dockipass:docker", "docker"], shell=False),
            call(["multipass", "alias", "dockipass:docker-compose",
                 "docker-compose"], shell=False)
        ]

        mock_run_cmd.assert_has_calls(calls)

    def test_with_more_disk(self, mock_run_cmd, mopen):
        launch(disk="40G")

        calls = [
            call(["multipass", "launch", "-c", "2", "-m", "2G", "-d", "40G", "-n",
                 "dockipass", "20.04", "--cloud-init", f"\"cloud-init-config/amd64.yaml\""], shell=True),
            call(["multipass", "mount", "/Users/", "dockipass"], shell=False),
            call(["multipass", "alias", "dockipass:docker", "docker"], shell=False),
            call(["multipass", "alias", "dockipass:docker-compose",
                 "docker-compose"], shell=False)
        ]

        mock_run_cmd.assert_has_calls(calls)

    @patch("lib.multipass.get_name_from_config", return_value="test2")
    def test_launch_with_new_name(self, mock_name, mock_run_cmd, mopen):
        launched = launch(name="test2")

        self.assertFalse(launched)
        mock_run_cmd.assert_not_called()
