from lib.background_task import check_for_background_task, run_task_in_background, stop_task_in_background
import unittest
from unittest.mock import patch
import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)


def func():
    print("pop")


class BackroundTasks(unittest.TestCase):

    def test_check_for_valid_task(self):
        result = check_for_background_task(
            argv=["cmd", "background", "listen"])
        self.assertTrue(result)

    def test_check_for_invalid_task(self):
        result = check_for_background_task(
            argv=["cmd", "background", "listens"])
        self.assertFalse(result)

    def test_check_for_invalid_command(self):
        result = check_for_background_task(
            argv=["cmd", "backgrounder", "listens"])
        self.assertFalse(result)

        result = check_for_background_task(argv=["cmd", "backgrounder"])
        self.assertFalse(result)

    @patch("builtins.print")
    @patch("lib.commander.run", return_value=("13212 process1\n123132 process3\n123123 python3 ./dockipass.py background listen\n123413 tests2", True))
    @patch("lib.background_task.run_in_background")
    def test_dont_start_background_task_when_already_running_in_background(self, mock_run_in_bg, mock_run_cmd, mock_print):
        run_task_in_background("listen")
        mock_run_cmd.assert_called_with(["ps", "ax"], live=False)
        mock_run_in_bg.not_called("")
        mock_print.assert_not_called()

    @patch("lib.commander.run", return_value=("13212 process1\n123132 process3\n 123123 python3 ./dockipass.py background listen\n123413 tests2", True))
    @patch("lib.background_task.kill_process")
    def test_stop_task_running_in_background(self, mock_kill, mock_run_cmd):
        stop_task_in_background("listen")
        mock_run_cmd.assert_called_with(["ps", "ax"], live=False)
        mock_kill.assert_called_with(123123)

    @patch("lib.commander.run", return_value=("13212 process1\n123132 process3\n123413 tests2", True))
    @patch("lib.background_task.kill_process")
    def test_stop_task_not_running_in_background(self, mock_kill, mock_run_cmd):
        stop_task_in_background("listen")
        mock_run_cmd.assert_called_with(["ps", "ax"], live=False)
        mock_kill.assert_not_called()
