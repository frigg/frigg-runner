# -*- coding: utf8 -*-

import sys
import time

from clint import textui


def timeit(function):
    def wrapper(*args, **kwargs):
        t1 = time.time()
        res = function(*args, **kwargs)
        t2 = time.time()
        return (t2 - t1), res
    return wrapper


def exit(code):
    sys.exit(code)


def exit_build(success):
        if success:
            textui.puts(textui.colored.green('Build success'))
            exit(0)
        else:
            textui.puts(textui.colored.red('Build fail'))
            exit(1)


def newline():
    textui.puts('\n', newline=False)


def put_task_result(task_result, color):
    textui.puts(color('%s (%s%s)' % (task_result.task, round(task_result.time, ndigits=2), 's')))
