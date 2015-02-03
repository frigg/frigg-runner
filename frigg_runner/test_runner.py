# -*- coding: utf8 -*-

import unittest

from frigg_runner import __name__, __version__
from frigg_runner.runner import Runner
from frigg_runner.startup import welcome_message


class StartupTestCase(unittest.TestCase):

    def testWelcomeMessage(self):
        self.assertEquals(welcome_message(), '%s %s' % (__name__, __version__))


class RunnerTestCase(unittest.TestCase):

    def test_init(self):

        config_file = 'test_config.yaml'
        full_run = True

        runner = Runner(config_file=config_file, full_run=full_run)

        self.assertEquals(runner.config_file, config_file)
        self.assertEquals(runner.full_run, full_run)
