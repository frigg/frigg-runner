# -*- coding: utf8 -*-

import unittest

import mock

from frigg_runner import __name__, __version__
from frigg_runner.runner import DEFAULT_CONFIG_FILES, Runner
from frigg_runner.startup import welcome_message


class StartupTestCase(unittest.TestCase):

    def testWelcomeMessage(self):
        self.assertEquals(welcome_message(), '%s %s' % (__name__, __version__))


class RunnerTestCase(unittest.TestCase):

    def setUp(self):
        self.runner = Runner(None, False)

    def test_init(self):

        config_file = 'test_config.yaml'
        full_run = True

        runner = Runner(config_file=config_file, full_run=full_run)

        self.assertEquals(runner.config_file, config_file)
        self.assertEquals(runner.full_run, full_run)

    def test_get_config_name(self):
        config_file = 'test_config.yaml'
        patcher = mock.patch('os.path.isfile')

        def is_file(file):
            return file == config_file

        mock_thing = patcher.start()
        mock_thing.side_effect = is_file

        config_file = 'test_config.yaml'
        full_run = True

        # Valid config file
        runner = Runner(config_file=config_file, full_run=full_run)

        self.assertEqual(runner.get_config_file_name(), config_file)

        # Invalid config file, default file exist
        def default_exist(file):
            return file in DEFAULT_CONFIG_FILES

        mock_thing.side_effect = default_exist

        runner.config_file = None
        self.assertEqual(runner.get_config_file_name(), DEFAULT_CONFIG_FILES[0])

        # No files exist
        def false_only(file):
            return False

        mock_thing.side_effect = false_only
        self.assertIsNone(runner.get_config_file_name())

        mock_thing.stop()
