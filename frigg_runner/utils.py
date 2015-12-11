# -*- coding: utf8 -*-

import functools
import sys
import time

import click

from .constants import RED_COLOR, WHITE_COLOR


def timeit(function):
    """
    This decorator executes the function and takes the execution time.
    """
    @functools.wraps(function)
    def wrapper(*args, **kwargs):
        t1 = time.time()
        res = function(*args, **kwargs)
        t2 = time.time()
        return res, (t2 - t1)
    return wrapper


def exit(code):
    """
    Exit the program with the provided exit-code.
    """
    assert isinstance(code, int), 'The exit-code needs to be a integer'
    sys.exit(code)


def newline():
    """
    Print a newline.
    """
    click.echo('', nl=True)


def error(message, exception=None):
    """
    Print a error message and exceptions details if provided.
    """
    if exception:
        message += ' - {}'.format(str(exception))
    click.secho(message, color=RED_COLOR)


def write_output(message, new_line=True, color=WHITE_COLOR):
    """
    Print a message in the console.
    """
    click.secho(message, color=color, nl=new_line)
