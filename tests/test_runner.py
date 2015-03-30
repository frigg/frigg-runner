# -*- coding: utf-8 -*-
import os
import sys
import unittest

import invoke
import mock
from clint.textui import colored
from frigg import projects
from invoke.exceptions import Failure
from invoke.runner import Result

from frigg_runner.runner import Runner


class RunnerTestCase(unittest.TestCase):

    @mock.patch('frigg.projects.build_settings')
    def test_runner_init(self, mock_run):
        """
        Test init of the runner class
        """
        runner = Runner(True, True)

        self.assertTrue(runner.fail_fast)
        self.assertTrue(runner.verbose)
        self.assertEqual(runner.directory, os.getcwd())

        projects.build_settings.assert_called_once_with(runner.directory)

    def test_no_tasks(self):
        """
        No tasks, system exit.
        """
        def raise_runtime_error(*args, **kwargs):
            raise RuntimeError

        projects.build_settings = mock.Mock(side_effect=raise_runtime_error)

        self.assertRaises(SystemExit, Runner, False, False)

    @mock.patch('frigg_coverage.parse_coverage', side_effect=lambda *args, **kwargs: 10)
    @mock.patch('clint.textui.colored.blue')
    def test_coverage_success(self, mock_run, mock_run1):
        """
        Test coverage result print
        """
        runner = Runner(False, False)

        runner.coverage()
        colored.blue.assert_called_with('Coverage %s%s' % (round(10, ndigits=2), '%'))

    def test_coverage_no_config(self):
        """
        Make sure noe exception raises when the coverage config not exist
        """
        runner = Runner(False, False)
        del(runner.config['coverage'])
        runner.coverage()

    def test_coverage_invalid_config(self):
        """
        Test coverage function with invalid config
        """
        runner = Runner(False, False)
        runner.config['coverage'] = True
        runner.coverage()
        runner.config['coverage'] = {}
        runner.coverage()

    @mock.patch('invoke.run')
    @mock.patch('frigg.projects.build_settings')
    def test_run_command(self, mock_run, mock_run1):
        """
        Test function for running commands
        """
        runner = Runner(False, True)
        runner.run_task('echo "Hello"')
        invoke.run.assert_called_once_with('echo "Hello"', hide=None)

    @mock.patch('frigg.projects.build_settings')
    def test_run_command_failure(self, mock_run):
        """
        Test function for command exec when the invoke return a Failure object
        """
        def raise_failure(*args, **kwargs):
            raise Failure('Custom result')
        invoke.run = mock.Mock(side_effect=raise_failure)

        runner = Runner(False, False)
        function_time, result = runner.run_task('echo "Hello"')
        invoke.run.assert_called_once_with('echo "Hello"', hide=True)
        self.assertEqual(result, 'Custom result')
        self.assertIsNotNone(function_time)

    @mock.patch('frigg.projects.build_settings')
    def test_run_command_exit(self, mock_run):
        """
        Test function for command exec when invoke exits
        """
        def raise_failure(*args, **kwargs):
            sys.exit(1)
        invoke.run = mock.Mock(side_effect=raise_failure)

        runner = Runner(False, False)
        function_time, result = runner.run_task('echo "Hello"')
        invoke.run.assert_called_once_with('echo "Hello"', hide=True)
        self.assertIsNone(result)

    @mock.patch('frigg.projects.build_settings')
    def test_handle_result(self, mock_run):
        """
        Test sysexit when the build is done.
        """
        runner = Runner(False, False)

        res1 = Result('', '', True, None)
        res1.task = 'tox'
        res1.time = 1
        res2 = Result('', '', False, None)
        res2.task = 'flake8'
        res2.time = 2

        try:
            runner.handle_results([
                res1, res2
            ])
        except SystemExit as sys_exit:
            self.assertEqual(sys_exit.code, 1)

        try:
            runner.handle_results([
                res2
            ])
        except SystemExit as sys_exit:
            self.assertEqual(sys_exit.code, 0)

        self.assertRaises(SystemExit, runner.handle_results, [res1, res2])

    @mock.patch('frigg.projects.build_settings')
    def test_run(self, mock_run):
        """
        Test the run function
        """
        runner = Runner(False, False)

        runner.config = {
            'tasks': [
                'flake8',
                'tox'
            ]
        }

        def create_result(*args, **kwargs):
            return 1, Result('', '', True, None)

        runner.run_task = mock.Mock(side_effect=create_result)
        runner.handle_results = mock.Mock()
        runner.run()
        runner.handle_results.assert_called_once()

    @mock.patch('frigg.projects.build_settings')
    def test_run_verbose(self, mock_run):
        """
        Test the run function
        """
        runner = Runner(False, True)

        runner.config = {
            'tasks': [
                'flake8',
                'tox'
            ]
        }

        def create_result(*args, **kwargs):
            return 1, Result('', '', True, None)

        runner.run_task = mock.Mock(side_effect=create_result)
        runner.handle_results = mock.Mock()
        runner.run()
        runner.handle_results.assert_called_once()

    @mock.patch('frigg.projects.build_settings')
    def test_run_fail_fast(self, mock_run):
        """
        Test the run function
        """
        runner = Runner(True, False)

        runner.config = {
            'tasks': [
                'flake8',
                'tox'
            ]
        }

        def create_result(*args, **kwargs):
            return 1, Result('', '', True, None)

        runner.run_task = mock.Mock(side_effect=create_result)
        runner.handle_results = mock.Mock()
        self.assertRaises(SystemExit, runner.run)
        runner.handle_results.assert_called_once()
