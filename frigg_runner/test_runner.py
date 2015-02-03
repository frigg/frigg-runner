# -*- coding: utf8 -*-

import unittest

from frigg_runner.cli import main


class RunnerTestCase(unittest.TestCase):

    def testTrue(self):
        self.assertTrue(main())
