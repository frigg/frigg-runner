# -*- coding: utf-8 -*-
import unittest

import mock
from click.testing import CliRunner

from frigg_runner.cli import main


@mock.patch('frigg_runner.cli.Runner')
class CLITests(unittest.TestCase):
    """
    This class tests the cli module.
    """

    def setUp(self):
        self.runner = CliRunner()

    def test_run(self, mock_runner):
        self.runner.invoke(main)
        mock_runner.assert_called_once_with(
            failfast=False,
            verbose=False,
            path=None,
            setup=False
        )

    def test_run_with_failfast(self, mock_runner):
        self.runner.invoke(main, ['--failfast'])
        mock_runner.assert_called_once_with(
            failfast=True,
            verbose=False,
            path=None,
            setup=False
        )

    def test_run_with_verbose(self, mock_runner):
        self.runner.invoke(main, ['--verbose'])
        mock_runner.assert_called_once_with(
            failfast=False,
            verbose=True,
            path=None,
            setup=False,
        )

    def test_run_with_path(self, mock_runner):
        self.runner.invoke(main, ['--path', '/tmp'])
        mock_runner.assert_called_once_with(failfast=False, verbose=False, path='/tmp', setup=False)
        mock_runner.assert_called_once_with(
            failfast=False,
            verbose=False,
            path='/tmp',
            setup=False,
        )

    def test_run_with_setup(self, mock_runner):
        self.runner.invoke(main, ['--setup'])
        mock_runner.assert_called_once_with(
            failfast=False,
            verbose=False,
            path=None,
            setup=True,
        )
