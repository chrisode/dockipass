from lib.docker import get_ports
import unittest
from unittest.mock import patch, Mock
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


class TestDocker(unittest.TestCase):

    @patch("lib.docker.run", Mock(return_value=docker_output(["8080"])))
    def test_get_docker_ports_should_return_ports(self):
        ports = get_ports()
        self.assertEqual(ports, ["8080"])
