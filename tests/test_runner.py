# -*- coding: utf-8 -*-
import os
import sys
import unittest

import mock
from invoke.exceptions import Failure
from invoke.runner import Result

from frigg_runner.runner import Runner


class RunnerTestCase(unittest.TestCase):

    @mock.patch('frigg.projects.build_settings')
    def test_runner_init(self, mock_build_settings):
        """
        Test init of the runner class
        """
        runner = Runner(True, True)

        self.assertTrue(runner.fail_fast)
        self.assertTrue(runner.verbose)
        self.assertEqual(runner.directory, os.getcwd())

        mock_build_settings.assert_called_once_with(runner.directory)

    @mock.patch('os.path.exists', side_effect=lambda *args, **kwargs: False)
    @mock.patch('frigg.projects.build_settings')
    def test_runner_init_cwd_not_found(self, mock_build_settings, mock_exists):
        """
        Test init of the runner class
        """

        self.assertRaises(SystemExit, Runner, True, True, '/tmp/doesnotexcist')

    @mock.patch('frigg.projects.build_settings', side_effect=RuntimeError)
    def test_no_tasks(self, mock_build_settings):
        """
        No tasks, system exit.
        """
        self.assertRaises(SystemExit, Runner, False, False)

    @mock.patch('frigg_coverage.parse_coverage', side_effect=lambda *args, **kwargs: 10)
    @mock.patch('clint.textui.colored.blue')
    def test_coverage_success(self, mock_blue, mock_parse_coverage):
        """
        Test coverage result print
        """
        runner = Runner(False, False)

        runner.coverage()
        mock_blue.assert_called_with('Coverage %s%s' % (round(10, ndigits=2), '%'))

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
    def test_run_command(self, mock_build_settings, mock_run):
        """
        Test function for running commands
        """
        runner = Runner(False, True, '/tmp')
        runner.run_task('echo "Hello"')
        mock_run.assert_called_once_with('cd %s && echo "Hello"' % runner.directory, hide=None)

    @mock.patch('frigg.projects.build_settings')
    @mock.patch('invoke.run', side_effect=Failure('Custom result'))
    def test_run_command_failure(self, mock_run, mock_build_settings):
        """
        Test function for command exec when the invoke return a Failure object
        """

        runner = Runner(False, False, '/tmp')
        function_time, result = runner.run_task('echo "Hello"')
        mock_run.assert_called_once_with('cd %s && echo "Hello"' % runner.directory, hide=True)
        self.assertEqual(result, 'Custom result')
        self.assertIsNotNone(function_time)

    @mock.patch('frigg.projects.build_settings')
    @mock.patch('invoke.run', side_effect=lambda *args, **kwargs: sys.exit(1))
    def test_run_command_exit(self, mock_run, mock_build_settings):
        """
        Test function for command exec when invoke exits
        """
        runner = Runner(False, False, '/tmp')
        function_time, result = runner.run_task('echo "Hello"')
        mock_run.assert_called_once_with('cd %s && echo "Hello"' % runner.directory, hide=True)
        self.assertIsNone(result)

    @mock.patch('frigg.projects.build_settings')
    def test_handle_result(self, mock_build_settings):
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
    def test_run(self, mock_build_settings):
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

        runner.run_task = mock.Mock(
            side_effect=lambda *args, **kwargs: (1, Result('', '', True, None))
        )
        runner.handle_results = mock.Mock()
        runner.run()
        runner.handle_results.assert_called_once()

    @mock.patch('frigg.projects.build_settings')
    def test_run_verbose(self, mock_build_settings):
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

        runner.run_task = mock.Mock(
            side_effect=lambda *args, **kwargs: (1, Result('', '', True, None))
        )
        runner.handle_results = mock.Mock()
        runner.run()
        runner.handle_results.assert_called_once()

    @mock.patch('frigg.projects.build_settings')
    def test_run_fail_fast(self, mock_build_settings):
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

        runner.run_task = mock.Mock(
            side_effect=lambda *args, **kwargs: (1, Result('', '', True, None))
        )
        runner.handle_results = mock.Mock()
        self.assertRaises(SystemExit, runner.run)
        runner.handle_results.assert_called_once()
