# -*- coding: utf8 -*-
import time
import unittest

import mock
from clint import textui
from invoke.runner import Result

from frigg_runner.utils import exit, exit_build, newline, put_task_result, timeit


class UtilsTestCase(unittest.TestCase):

    @mock.patch('clint.textui.puts')
    def test_newline(self, mock_run):
        newline()
        textui.puts.assert_called_once_with('\n', newline=False)

    def test_exit(self):
        self.assertRaises(SystemExit, exit, 0)

        try:
            exit(3)
        except SystemExit as sys_exit:
            self.assertEqual(sys_exit.code, 3)

    def test_time_it(self):

        @timeit
        def sleep():
            time.sleep(1)
            return True

        execute_time, result = sleep()

        self.assertAlmostEqual(round(execute_time), 1)
        self.assertTrue(result)

    @mock.patch('clint.textui.puts')
    def test_put_task_result(self, mock_run):
        result = Result(None, None, None, None)
        result.time = 2.9843
        result.task = 'tox'

        # Use str to mock the color wrapper.
        color = str
        put_task_result(result, color)
        textui.puts.assert_called_once_with(color(
            '%s (%s%s)' % (result.task, round(result.time, ndigits=2), 's')))

    @mock.patch('clint.textui.puts')
    def test_exit_build(self, mock_run):
        self.assertRaises(SystemExit, exit_build, False)
        textui.puts.assert_called_once()

        try:
            exit_build(True)
        except SystemExit as sys_exit:
            self.assertEqual(sys_exit.code, 0)

        try:
            exit_build(False)
        except SystemExit as sys_exit:
            self.assertEqual(sys_exit.code, 1)
