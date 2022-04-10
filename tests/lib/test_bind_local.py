from lib.bind_local import bind_local, forward, add_forwared_port, get_forwared_ports, unbind_all
from lib.config import set_name
import unittest
from unittest.mock import patch, Mock
import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


forwarded_file = "forwared_ports.json"


@patch("lib.config._get_config_from_file", Mock(return_value={}))
@patch("lib.config._update_config_file", Mock())
class TestBindLocalSetup(unittest.TestCase):

    def setUp(self):
        if os.path.exists(forwarded_file):
            with open(forwarded_file, "r") as file:
                self.orgForwaredPorts = file.read()

            os.remove(forwarded_file)

    def tearDown(self):
        if self.orgForwaredPorts:
            with open(forwarded_file, "w+") as file:
                file.write(self.orgForwaredPorts)

    @patch("lib.bind_local.forwared_ports", {})
    def test_should_return_forwared_ports_when_file_doesnt_exist(self):
        forwared_ports = get_forwared_ports()
        self.assertEqual(forwared_ports, {})

    @patch("lib.bind_local.forwared_ports", {})
    def test_should_create_forwared_json_if_file_doesnt_exist(self):
        add_forwared_port(8080, 11)
        self.assertTrue(os.path.exists(forwarded_file))


@patch("lib.config._get_config_from_file", Mock(return_value={}))
@patch("lib.config._update_config_file", Mock())
class TestBindLocalHelpers(unittest.TestCase):

    def setUp(self):
        if os.path.exists(forwarded_file):
            with open(forwarded_file, "r") as file:
                self.orgForwaredPorts = file.read()

            with open(forwarded_file, "w+") as file:
                file.write("{}")

    def tearDown(self):
        if self.orgForwaredPorts:
            with open(forwarded_file, "w+") as file:
                file.write(self.orgForwaredPorts)

    @patch("lib.bind_local.run_in_background", return_value=11)
    def test_forward_runs_socat(self, mock_run_in_bg):
        forward(8080)
        mock_run_in_bg.assert_called_once()

    @patch("lib.bind_local.run_in_background", return_value=11)
    def test_forward_has_forwarded_the_given_port(self, mock_run_in_bg):
        forward(8080)
        self.assertTrue(str(mock_run_in_bg.call_args[0]).find("8080") > -1)


@patch("lib.config._get_config_from_file", Mock(return_value={}))
@patch("lib.config._update_config_file", Mock())
class TestBindLocal(unittest.TestCase):

    def setUp(self):
        if os.path.exists(forwarded_file):
            with open(forwarded_file, "r") as file:
                self.orgForwaredPorts = file.read()

            with open(forwarded_file, "w+") as file:
                file.write("{}")

    def tearDown(self):
        if self.orgForwaredPorts:
            with open(forwarded_file, "w+") as file:
                file.write(self.orgForwaredPorts)

    @patch("lib.bind_local.forward")
    @patch("lib.bind_local.kill_process")
    @patch("lib.bind_local.get_ports", return_value=["8080"])
    def test_bind_local(self, mock_ports, mock_kill, mock_forward):
        bind_local()

        # Forwared ports should have been called
        mock_ports.assert_called()

        # It should forward the port
        mock_forward.assert_called_with("8080")

        # It should not have killed any process
        mock_kill.assert_not_called()

    @patch("lib.bind_local.forward")
    @patch("lib.bind_local.kill_process")
    @patch("lib.bind_local.get_ports", return_value=[])
    def test_bind_local_kill(self, mock_ports, mock_kill, mock_forward):
        # It has ports already forwared
        with open(forwarded_file, "w+") as file:
            file.write("{\"8080\":\"11\"}")

        bind_local()
        # Forward should not be called
        mock_forward.assert_not_called()

        # Kill the running forwarer
        mock_kill.assert_called_with("11")

        # Should remove the forwared port
        with open(forwarded_file, "r") as file:
            output = file.read()
            self.assertEqual(output, "{}")

    @patch("lib.bind_local.forward")
    @patch("lib.bind_local.kill_process")
    @patch("lib.bind_local.get_ports", return_value=["8080"])
    def test_bind_local_no_change(self, mock_ports, mock_kill, mock_forward):

        json = "{\"8080\":\"11\"}"

        # It has ports already forwared
        with open(forwarded_file, "w+") as file:
            file.write(json)

        bind_local()
        # Forward should not be called
        mock_forward.assert_not_called()

        # No forwarer should be killed
        mock_kill.assert_not_called()

        # Forwared.json should not have been changed
        with open(forwarded_file, "r") as file:
            output = file.read()
            self.assertEqual(output, json)

    @patch("lib.bind_local.run_in_background")
    @patch("lib.bind_local.add_forwared_port")
    @patch("lib.bind_local.get_ports", return_value=["8080"])
    @patch("builtins.print")
    def test_bind_local_verbose(self, mock_print, mock_ports, mock_bg, mock_forward):
        bind_local(verbose=True)

        mock_print.assert_called()

    @patch("lib.bind_local.run_in_background")
    @patch("lib.bind_local.add_forwared_port")
    @patch("lib.bind_local.get_ports", return_value=["8080"])
    @patch("builtins.print")
    def test_bind_local_no_verbose(self, mock_print, mock_ports, mock_bg, mock_forward):
        bind_local(verbose=False)

        mock_print.assert_not_called()

    @patch("lib.commander.run", return_value="123123 testar2\n11 s008  S      0:00.01 socat tcp-listen:8080,bind=localhost,reuseaddr,fork tcp:dockipass-alias.local:8080\n124123 testtest")
    @patch("lib.bind_local.kill_process")
    def test_unbind_all(self, mock_kill, mock_run):
        unbind_all()
        mock_run.assert_called_with(["ps", "ax"], live=False)
        mock_kill.assert_called_with(11)

    @patch("lib.bind_local.run_in_background", return_value="1")
    @patch("lib.bind_local.get_ports", return_value=["8080"])
    def test_bind_local_run_called_with_name(self, mock_ports, mock_run):
        set_name("kaka")
        bind_local()
        mock_run.assert_called()
        called_with = " ".join(mock_run.call_args[0][0])
        self.assertTrue(called_with.find("kaka") > -1)
