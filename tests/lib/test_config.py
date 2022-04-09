from lib.config import DEFAULT_NAME, set_name, get_name, _reset
import unittest
from unittest.mock import patch, Mock
import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


@patch("lib.config._get_config_from_file", return_value={})
@patch("lib.config._update_config_file")
class TestConfig(unittest.TestCase):

    @classmethod
    @patch("lib.config._update_config_file", Mock())
    def setUpClass(cls):
        _reset()

    @classmethod
    @patch("lib.config._update_config_file", Mock())
    def tearDownClass(cls):
        _reset()

    def test_default_name(self, mock_update, mock_get):
        self.assertEqual(DEFAULT_NAME, "dockipass")


    def test_name_when_not_set(self, mock_update, mock_get):
        mock_get.assert_not_called()
        self.assertEqual(get_name(), None)
        mock_get.assert_called()


    def test_name_when_set(self, mock_update, mock_get):
        set_name("test2")
        mock_update.assert_called()

        self.assertEqual(get_name(), "test2")
