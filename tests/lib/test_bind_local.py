from lib.bind_local import bind_local, get_docker_ports, forward, add_forwared_port, get_forwared_ports
import unittest
from unittest.mock import patch
import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


def docker_output(ports):

    output = []

    for port in ports:
        return f"runningÅ0.0.0.0:{port}->80/tcp, :::{port}->80/tcp"

    return "".join(output)


forwarded_file = "forwared_ports.json"


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

    @patch("lib.bind_local.run", return_value=docker_output(["8080"]))
    def test_get_docker_ports_should_return_ports(self, mock_run):
        ports = get_docker_ports()
        self.assertEqual(ports, [8080])

    @patch("lib.bind_local.run_in_background", return_value=11)
    def test_forward_runs_socat(self, mock_run_in_bg):
        forward(8080)
        mock_run_in_bg.assert_called_once()

    @patch("lib.bind_local.run_in_background", return_value=11)
    def test_forward_has_forwarded_the_given_port(self, mock_run_in_bg):
        forward(8080)
        self.assertTrue(str(mock_run_in_bg.call_args[0]).find("8080") > -1)


@patch("lib.bind_local.forward")
@patch("lib.bind_local.kill_process")
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

    @patch("lib.bind_local.get_docker_ports", return_value=[8080])
    def test_bind_local(self, mock_ports, mock_kill, mock_forward):
        bind_local()

        # Forwared ports should have been called
        mock_ports.assert_called()

        # It should forward the port
        mock_forward.assert_called_with(8080)

        # It should not have killed any process
        mock_kill.assert_not_called()

    @patch("lib.bind_local.get_docker_ports", return_value=[])
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

    @patch("lib.bind_local.get_docker_ports", return_value=["8080"])
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
