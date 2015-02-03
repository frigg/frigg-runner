# -*- coding: utf8 -*-

import unittest

from frigg_runner import __name__, __version__
from frigg_runner.startup import welcome_message


class StartupTestCase(unittest.TestCase):

    def testWelcomeMessage(self):
        self.assertEquals(welcome_message(), '%s %s' % (__name__, __version__))
