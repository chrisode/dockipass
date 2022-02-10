from lib.background_task import check_for_background_task, run_task
import unittest
from unittest.mock import patch, call
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
    @patch("lib.background_task.available_background_tasks", {"listen": func})
    def test_run_task(self, mock_print):
        run_task("listen")

        mock_print.assert_called()
