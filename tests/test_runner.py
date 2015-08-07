# -*- coding: utf-8 -*-
import os
import sys
import unittest
from unittest import skip

import mock
import six
from invoke.exceptions import Failure
from invoke.runner import Result

from frigg_runner.runner import Runner, runner_wrapper

OPEN_MODULE = 'builtins.open' if six.PY3 else '__builtin__.open'
RUN_TASK_RESULT = (1, Result('', '', True, None))


class RunnerTestCase(unittest.TestCase):

    @mock.patch('frigg_settings.build_settings')
    def test_runner_init(self, mock_build_settings):
        """
        Test init of the runner class
        """
        runner = Runner(failfast=True, verbose=True)

        self.assertTrue(runner.fail_fast)
        self.assertTrue(runner.verbose)
        self.assertEqual(runner.directory, os.getcwd())

        mock_build_settings.assert_called_once_with(runner.directory, runner_wrapper)

    @mock.patch('os.path.exists', side_effect=lambda *args, **kwargs: False)
    @mock.patch('frigg_settings.build_settings')
    def test_runner_init_cwd_not_found(self, mock_build_settings, mock_exists):
        """
        Test init of the runner class
        """

        self.assertRaises(SystemExit, Runner, True, True, '/tmp/doesnotexcist')

    @mock.patch('frigg_settings.build_settings', side_effect=RuntimeError)
    def test_no_tasks(self, mock_build_settings):
        """
        No tasks, system exit.
        """
        self.assertRaises(SystemExit, Runner, False, False)

    @mock.patch('frigg_settings.build_settings', side_effect=TypeError)
    def test_invalid_frigg_file_format(self, mock_build_settings):
        """
        Test invalid yaml format in frigg file
        """
        self.assertRaises(SystemExit, Runner, False, False)

    @mock.patch(OPEN_MODULE, side_effect=lambda *args, **kwargs: FileIO('coverage_report'))
    @mock.patch('frigg_settings.build_settings', side_effect=lambda *args, **kwargs: {})
    @mock.patch('os.path.exists', side_effect=lambda *args, **kwargs: True)
    @mock.patch('frigg_coverage.parse_coverage', side_effect=lambda *args, **kwargs: 10)
    def test_coverage_success(self, mock_parse_coverage, mock_exists, mock_build_settings,
                              mock_open):
        """
        Test coverage result print
        """
        runner = Runner()
        runner.config['coverage'] = {
            'path': 'coverage.xml',
            'parser': 'python'
        }
        runner.coverage()

        mock_parse_coverage.assert_called_with(
            'coverage_report',
            runner.config['coverage']['parser']
        )

    @mock.patch('frigg_settings.build_settings', side_effect=lambda *args, **kwargs: {})
    @mock.patch('os.path.exists', side_effect=lambda *args, **kwargs: True)
    def test_coverage_no_config(self, mock_exists, mock_build_settings):
        """
        Make sure no exception raises when the coverage config not exist
        """
        runner = Runner()
        if 'coverage' in runner.config.keys():
            del(runner.config['coverage'])
        runner.coverage()

    @mock.patch('sys.exit')
    @mock.patch('frigg_settings.build_settings', side_effect=lambda *args, **kwargs: {})
    @mock.patch('os.path.exists', side_effect=lambda *args, **kwargs: True)
    def test_coverage_invalid_config(self, mock_exists, mock_build_settings, mock_exit):
        """
        Test coverage function with invalid config
        """
        runner = Runner()
        runner.config['coverage'] = True
        runner.coverage()
        mock_exit.assert_called_once_with(1)

    @mock.patch('invoke.run')
    @mock.patch('frigg_settings.build_settings')
    def test_run_command(self, mock_build_settings, mock_run):
        """
        Test function for running commands
        """
        runner = Runner(verbose=True, path='/tmp')
        runner.run_task('echo "Hello"')
        mock_run.assert_called_once_with('cd %s && echo "Hello"' % runner.directory, hide=False,
                                         encoding='utf8', pty=True)

    @mock.patch('invoke.run')
    @mock.patch('frigg_settings.build_settings',
                side_effect=lambda *args, **kwargs: {'verbose_tasks': ['echo "Hello"']})
    def test_run_command_verbose_task(self, mock_build_settings, mock_run):
        """
        Test function for running commands
        """
        runner = Runner(failfast=False, verbose=False, path='/tmp')
        runner.run_task('echo "Hello"')
        mock_run.assert_called_once_with('cd %s && echo "Hello"' % runner.directory, hide=False,
                                         encoding='utf8', pty=True)

    @mock.patch('frigg_settings.build_settings')
    @mock.patch('invoke.run', side_effect=Failure('Custom result'))
    def test_run_command_failure(self, mock_run, mock_build_settings):
        """
        Test function for command exec when the invoke return a Failure object
        """

        runner = Runner(path='/tmp')
        function_time, result = runner.run_task('echo "Hello"')
        mock_run.assert_called_once_with('cd %s && echo "Hello"' % runner.directory, hide=True,
                                         encoding='utf8', pty=True)
        self.assertEqual(result, 'Custom result')
        self.assertIsNotNone(function_time)

    @mock.patch('frigg_settings.build_settings')
    @mock.patch('invoke.run', side_effect=lambda *args, **kwargs: sys.exit(1))
    def test_run_command_exit(self, mock_run, mock_build_settings):
        """
        Test function for command exec when invoke exits
        """
        runner = Runner(path='/tmp')
        function_time, result = runner.run_task('echo "Hello"')
        mock_run.assert_called_once_with('cd %s && echo "Hello"' % runner.directory, hide=True,
                                         encoding='utf8', pty=True)
        self.assertIsNone(result)

    @mock.patch('frigg_runner.runner.Runner.coverage')
    @mock.patch('frigg_settings.build_settings')
    def test_handle_result(self, mock_build_settings, mock_coverage):
        """
        Test sysexit when the build is done.
        """
        runner = Runner(setup=True)

        res1 = Result('', '', True, None)
        res1.task = 'tox'
        res1.time = 1
        res2 = Result('', '', False, None)
        res2.task = 'flake8'
        res2.time = 2
        res3 = Result('', '', True, None)
        res3.task = 'bower install'
        res3.time = 3
        res4 = Result('', '', False, None)
        res4.task = 'exit 1'
        res4.time = 4

        try:
            runner.handle_results([res1, res2], [res3, res4])
        except SystemExit as sys_exit:
            self.assertEqual(sys_exit.code, 1)

        self.assertTrue(mock_coverage.called)

        try:
            runner.handle_results([res2], [res3, res4])
        except SystemExit as sys_exit:
            self.assertEqual(sys_exit.code, 0)

        self.assertRaises(SystemExit, runner.handle_results, [res1, res2], [res3, res4])

    @mock.patch('frigg_runner.runner.Runner.handle_results')
    @mock.patch('frigg_settings.build_settings')
    @mock.patch('frigg_runner.runner.Runner.run_task', lambda *args, **kwargs: RUN_TASK_RESULT)
    def test_run(self, mock_build_settings, mock_handle_results):
        """
        Test the run function
        """
        runner = Runner()

        runner.config = {
            'tasks': [
                'flake8',
                'tox'
            ]
        }

        runner.run()
        self.assertTrue(mock_handle_results.called)

    @mock.patch('frigg_runner.runner.Runner.handle_results')
    @mock.patch('frigg_settings.build_settings')
    @mock.patch('frigg_runner.runner.Runner.run_task', lambda *args, **kwargs: RUN_TASK_RESULT)
    def test_run_verbose(self, mock_build_settings, mock_handle_results):
        """
        Test the run function
        """
        runner = Runner(verbose=True)

        runner.config = {
            'tasks': [
                'flake8',
                'tox'
            ]
        }

        runner.run()
        self.assertTrue(mock_handle_results.called)

    @skip('This test has never worked, just silently failed.'
          'Because failfast makes the app exit.')
    @mock.patch('frigg_runner.runner.Runner.handle_results')
    @mock.patch('frigg_settings.build_settings')
    @mock.patch('frigg_runner.runner.Runner.run_task', lambda *args, **kwargs: RUN_TASK_RESULT)
    def test_run_fail_fast(self, mock_build_settings, mock_handle_results):
        """
        Test the run function
        """
        runner = Runner(failfast=True)

        runner.config = {
            'tasks': [
                'flake8',
                'tox'
            ]
        }

        self.assertRaises(SystemExit, runner.run)
        self.assertTrue(mock_handle_results.called)

    @mock.patch('frigg_runner.runner.Runner.handle_results')
    @mock.patch('frigg_runner.runner.Runner.run_task', lambda *args, **kwargs: RUN_TASK_RESULT)
    def test_run_setup_tasks(self, mock_handle_results):
        """
        Test the run function with setup tasks
        """
        runner = Runner(setup=True)

        runner.config = {
            'tasks': [],
            'setup_tasks': [
                'bower install'
            ]
        }

        runner.run()
        self.assertTrue(mock_handle_results.called)


class FileIO(six.StringIO):
    if six.PY2:
        def __exit__(self, *args, **kwargs):
            self.close()

        def __enter__(self):
            return self
