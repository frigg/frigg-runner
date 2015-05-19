# -*- coding: utf8 -*-
import time
import unittest

import mock
from invoke.runner import Result

from frigg_runner.utils import exit, exit_build, newline, print_task, put_task_result, timeit


class UtilsTestCase(unittest.TestCase):

    @mock.patch('click.echo')
    def test_newline(self, mock_echo):
        newline()
        mock_echo.assert_called_once_with('', nl=True)

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

    @mock.patch('click.secho')
    def test_put_task_result(self, mock_secho):
        result = Result(None, None, None, None)
        result.time = 2.9843
        result.task = 'tox'

        color = 'red'
        put_task_result(result, color)
        mock_secho.assert_called_once_with('  # %s (%s%s) ' % (result.task,
                                                               round(result.time, ndigits=2),
                                                               's'), fg=color)

    def test_exit_build(self):
        self.assertRaises(SystemExit, exit_build, False)

        try:
            exit_build(True)
        except SystemExit as sys_exit:
            self.assertEqual(sys_exit.code, 0)

        try:
            exit_build(False)
        except SystemExit as sys_exit:
            self.assertEqual(sys_exit.code, 1)

    def test_task_print(self):
        self.assertEqual(print_task('test'), ':  test')
        self.assertEqual(print_task(None), '')
