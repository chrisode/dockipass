
from lib.multipass import start, stop, restart, launch, delete, set_name, _reset, get_info, check_aliases
import unittest
from unittest.mock import patch, call, mock_open, Mock
import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


@patch("lib.multipass.run_cmd", return_value=("{}", True))
@patch("lib.config._config.config", {})
@patch("lib.config._config.update_config_file", Mock())
class TestMultipass(unittest.TestCase):

    @classmethod
    @patch("lib.config._config.update_config_file", Mock())
    def setUpClass(cls):
        _reset()

    @patch("lib.config._config.update_config_file", Mock())
    def tearDown(self):
        _reset()

    def test_start(self, mock_run_cmd):
        set_name("test")
        start()
        mock_run_cmd.assert_called_with(
            ["multipass", "start", "test"], shell=False, live=True)

    def test_restart(self, mock_run_cmd):
        set_name("test")
        restart()
        mock_run_cmd.assert_called_with(
            ["multipass", "restart", "test"], shell=False, live=True)

    def test_stop(self, mock_run_cmd):
        set_name("test")
        stop()
        mock_run_cmd.assert_called_with(
            ["multipass", "stop", "test"], shell=False, live=True)

    @patch("builtins.open", new_callable=mock_open, read_data="#!/bin/sh\n\ndocker-compose -- awd")
    @patch("lib.multipass.ARCHITECTURE", "amd64")
    def test_launch(self, mock_mock_open, mock_run_cmd):
        set_name(None)
        launch("test")

        calls = [
            call(["multipass", "launch", "-c", "2", "-m", "2G", "-d", "20G", "-n",
                 "test", "20.04", "--cloud-init", f"\"cloud-init-config/amd64.yaml\""], shell=True, live=True),
            call(["multipass", "mount", "/Users/", "test"],
                 shell=False, live=True),
            call(["multipass", "alias", "test:docker",
                 "docker"], shell=False, live=True),
            call(["multipass", "alias", "test:docker-compose",
                 "docker-compose"], shell=False, live=True)
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
            call(["multipass", "unalias", "docker"], shell=False, live=True),
            call(["multipass", "unalias", "docker-compose"],
                 shell=False, live=True),
            call(["multipass", "delete", "test"], shell=False, live=True),
            call(["multipass", "purge"], shell=False, live=True),
        ]

        mock_run_cmd.assert_has_calls(calls)

    def test_info(self, mock_run_cmd):
        set_name("test")
        get_info()

        calls = [
            call(["multipass", "info", "test", "--format", "json"],
                 shell=False, live=False),
        ]

        mock_run_cmd.assert_has_calls(calls)

    def test_check_alias(self, mock_run_cmd):
        set_name("test")
        mock_run_cmd.return_value = ("""{
        "aliases": [
        {
            "alias": "docker",
            "command": "docker",
            "instance": "test"
        },
        {
            "alias": "docker-compose",
            "command": "docker-compose",
            "instance": "test"
        }
    ]
}""", True)

        checked = check_aliases()

        mock_run_cmd.assert_called()
        self.assertTrue(checked)


    def test_check_alias_with_aliases_for_other_instance(self, mock_run_cmd):
        set_name("test")
        mock_run_cmd.return_value = ("""{
        "aliases": [
        {
            "alias": "docker",
            "command": "docker",
            "instance": "test2"
        },
        {
            "alias": "docker-compose",
            "command": "docker-compose",
            "instance": "test2"
        }
    ]
}""", True)

        checked = check_aliases()
        self.assertFalse(checked)

    def test_check_alias_with_no_aliases(self, mock_run_cmd):
        set_name("test")
        mock_run_cmd.return_value = ("{\"aliases\": []}", True)

        checked = check_aliases()
        self.assertFalse(checked)

    def test_check_alias_with_only_one_alias(self, mock_run_cmd):
        set_name("test")
        mock_run_cmd.return_value = ("""{
        "aliases": [
        {
            "alias": "docker",
            "command": "docker",
            "instance": "test"
        }
    ]
}""", True)

        checked = check_aliases()
        self.assertFalse(checked)


@patch("lib.multipass.ARCHITECTURE", "amd64")
@patch("builtins.open", new_callable=mock_open)
@patch("lib.multipass.run_cmd", return_value=True)
@patch("lib.config._config.config", {})
@patch("lib.config._config.update_config_file", Mock())
class TestLaunch(unittest.TestCase):

    @classmethod
    @patch("lib.config._config.update_config_file", Mock())
    def setUpClass(cls):
        _reset()

    @patch("lib.config._config.update_config_file", Mock())
    def tearDown(self):
        _reset()

    def test_with_default_name(self, mock_run_cmd, mopen):
        _reset()
        launch()

        calls = [
            call(["multipass", "launch", "-c", "2", "-m", "2G", "-d", "20G", "-n",
                 "dockipass", "20.04", "--cloud-init", f"\"cloud-init-config/amd64.yaml\""], shell=True, live=True),
            call(["multipass", "mount", "/Users/", "dockipass"],
                 shell=False, live=True),
            call(["multipass", "alias", "dockipass:docker",
                 "docker"], shell=False, live=True),
            call(["multipass", "alias", "dockipass:docker-compose",
                 "docker-compose"], shell=False, live=True)
        ]

        mock_run_cmd.assert_has_calls(calls)

    def test_with_non_default_cpu(self, mock_run_cmd, mopen):
        _reset()
        launch(cpu=4)

        calls = [
            call(["multipass", "launch", "-c", "4", "-m", "2G", "-d", "20G", "-n",
                 "dockipass", "20.04", "--cloud-init", f"\"cloud-init-config/amd64.yaml\""], shell=True, live=True),
            call(["multipass", "mount", "/Users/", "dockipass"],
                 shell=False, live=True),
            call(["multipass", "alias", "dockipass:docker",
                 "docker"], shell=False, live=True),
            call(["multipass", "alias", "dockipass:docker-compose",
                 "docker-compose"], shell=False, live=True)
        ]

        mock_run_cmd.assert_has_calls(calls)

    def test_with_more_memory(self, mock_run_cmd, mopen):
        _reset()
        launch(memory="4G")

        calls = [
            call(["multipass", "launch", "-c", "2", "-m", "4G", "-d", "20G", "-n",
                 "dockipass", "20.04", "--cloud-init", f"\"cloud-init-config/amd64.yaml\""], shell=True, live=True),
            call(["multipass", "mount", "/Users/", "dockipass"],
                 shell=False, live=True),
            call(["multipass", "alias", "dockipass:docker",
                 "docker"], shell=False, live=True),
            call(["multipass", "alias", "dockipass:docker-compose",
                 "docker-compose"], shell=False, live=True)
        ]

        mock_run_cmd.assert_has_calls(calls)

    def test_with_more_disk(self, mock_run_cmd, mopen):
        _reset()
        launch(disk="40G")

        calls = [
            call(["multipass", "launch", "-c", "2", "-m", "2G", "-d", "40G", "-n",
                 "dockipass", "20.04", "--cloud-init", f"\"cloud-init-config/amd64.yaml\""], shell=True, live=True),
            call(["multipass", "mount", "/Users/", "dockipass"],
                 shell=False, live=True),
            call(["multipass", "alias", "dockipass:docker",
                 "docker"], shell=False, live=True),
            call(["multipass", "alias", "dockipass:docker-compose",
                 "docker-compose"], shell=False, live=True)
        ]

        mock_run_cmd.assert_has_calls(calls)

    @patch("lib.multipass.get_name_from_config", return_value="test2")
    def test_launch_with_new_name(self, mock_name, mock_run_cmd, mopen):
        launched = launch(name="test2")

        self.assertFalse(launched)
        mock_run_cmd.assert_not_called()
