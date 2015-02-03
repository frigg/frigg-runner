# -*- coding: utf8 -*-

from . import __name__, __version__


def welcome_message():
    return '%s %s' % (__name__, __version__)
