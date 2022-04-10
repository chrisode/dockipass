from lib.bind_local import bind_local, forward, unbind_all
from lib.config import set_name
import unittest
from unittest.mock import patch, Mock
import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


@patch("lib.config._config.config", {})
@patch("lib.config._config.update_config_file", Mock())
class TestBindLocalHelpers(unittest.TestCase):

    @patch("lib.bind_local.run_in_background", return_value=11)
    def test_forward_runs_socat(self, mock_run_in_bg):
        forward(8080)
        mock_run_in_bg.assert_called_once()

    @patch("lib.bind_local.run_in_background", return_value=11)
    def test_forward_has_forwarded_the_given_port(self, mock_run_in_bg):
        forward(8080)
        self.assertTrue(str(mock_run_in_bg.call_args[0]).find("8080") > -1)


@patch("lib.config._config.config", {})
@patch("lib.config._config.update_config_file", Mock())
class TestBindLocal(unittest.TestCase):

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
    @patch("lib.bind_local.get_ports", Mock(return_value=[]))
    @patch("lib.bind_local.get_forwarded_ports", return_value={"8080":"11"})
    @patch("lib.bind_local.set_forwarded_ports")
    def test_bind_local_kill(self, mock_set_forward, mock_forwared, mock_kill, mock_forward):
       
        bind_local()

        # It should have fetched forwared ports
        mock_forwared.assert_called()

        # Forward should not be called
        mock_forward.assert_not_called()

        # Kill the running forwarer
        mock_kill.assert_called_with("11")

        # Should remove the forwared port
        mock_set_forward.assert_called_with({})

    @patch("lib.bind_local.forward")
    @patch("lib.bind_local.kill_process")
    @patch("lib.bind_local.get_ports", return_value=["8080"])
    @patch("lib.bind_local.get_forwarded_ports", return_value={"8080":"11"})
    @patch("lib.bind_local.set_forwarded_ports")
    def test_bind_local_no_change(self, mock_set_forward, mock_forwared, mock_ports, mock_kill, mock_forward):

        json = "{\"8080\":\"11\"}"

        bind_local()

        # Forward should not be called
        mock_forward.assert_not_called()

        # It should have fetched forwared ports
        mock_forwared.assert_called()

        # No forwarer should be killed
        mock_kill.assert_not_called()

        # Forwared should not have been called
        mock_set_forward.assert_not_called()
       

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
