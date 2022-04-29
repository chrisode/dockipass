import unittest
from unittest.mock import patch, Mock, mock_open
import os
import sys

from lib.config import _reset, set_name
from lib.status import status

import json

from tests.test_helpers.common import get_data

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


def get_infodata(state="running"):
    data = json.loads(get_data("multipass-info.json"))

    instance = data.get("info").get("test")

    instance["state"] = state

    return json.dumps(data), True

@patch("lib.config._config.update_config_file", Mock())
class TestConfig(unittest.TestCase):

    @classmethod
    @patch("lib.config._config.update_config_file", Mock())
    def setUpClass(cls):
        _reset()

    @patch("lib.config._config.update_config_file", Mock())
    def setUp(self):
        set_name("test")

    @patch("lib.config._config.update_config_file", Mock())
    def tearDown(cls):
        _reset()

    @patch("lib.multipass.run_cmd", return_value=get_infodata())
    def test_status(self, mock_run):

        statusmsg = status()

        self.assertIn("VM Name:\t test\n", statusmsg)
        self.assertIn("State:\t\t running\n", statusmsg)

        mock_run.assert_called()

    
    @patch("lib.multipass.run_cmd", return_value=get_infodata("stopped"))
    def test_status_not_running(self, mock_run):

        statusmsg = status()

        self.assertIn("VM Name:\t test\n", statusmsg)
        self.assertIn("State:\t\t stopped\n", statusmsg)

        mock_run.assert_called()

    