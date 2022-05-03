from lib.config import DEFAULT_NAME, set_name, get_name, _reset, get_forwarded_ports, set_forwarded_ports, _config
import unittest
from unittest.mock import patch, Mock, mock_open
import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


class TestConfig(unittest.TestCase):

    @classmethod
    @patch("lib.config._config.update_config_file", Mock())
    def setUpClass(cls):
        _reset()

    @patch("lib.config._config.update_config_file", Mock())
    def tearDown(cls):
        _reset()

    def test_default_name(self):
        self.assertEqual(DEFAULT_NAME, "dockipass")

    @patch("lib.config.path.exists", Mock(return_value=True))
    @patch("builtins.open", new_callable=mock_open, read_data="{\"name\": \"test\"}")
    def test_get_config_behaviour(self, mock_open):
        _config.update_config_from_file()
        self.assertEqual(get_name(), "test")
        mock_open.assert_called_with('config/config.json', 'r')

    @patch("builtins.open", new_callable=mock_open)
    def test_update_config_behaviour(self, mock_open):
        set_name("test")
        self.assertEqual(get_name(), "test")
        mock_open.assert_called_with('config/config.json', 'w+')
        mock_file = mock_open()
        mock_file.write.assert_called_once_with("{\"name\": \"test\"}")

    @patch("lib.config._config.config", {})
    def test_name_when_not_set(self):
        self.assertEqual(get_name(), None)

    @patch("lib.config._config.update_config_file")
    def test_name_when_set(self, mock_update):
        set_name("test2")
        mock_update.assert_called()

        self.assertEqual(get_name(), "test2")

    @patch("lib.config._config.update_config_file")
    def test_set_forward(self, mock_update):
        set_forwarded_ports([8080, 8081])
        mock_update.assert_called()

    @patch("lib.config._config.config", {"forwarded_ports": [8080]})
    def test_get_forward(self):
        ports = get_forwarded_ports()
        self.assertEqual(ports, [8080])
