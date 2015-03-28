# -*- coding: utf-8 -*-
import unittest

import mock
from click.testing import CliRunner

from frigg_runner.cli import main


@mock.patch('frigg_runner.runner.Runner.__init__')
@mock.patch('frigg_runner.runner.Runner.run')
class CLITestCase(unittest.TestCase):

    def setUp(self):
        self.runner = CliRunner()

    def test_run(self, mock_run, mock_runner):
        self.runner.invoke(main)
        mock_run.assert_called_once()
        mock_runner.assert_called_once_with(failfast=False)

    def test_run_with_failfast(self, mock_run, mock_runner):
        self.runner.invoke(main, ['--failfast'])
        mock_run.assert_called_once()
        mock_runner.assert_called_once_with(failfast=True)
