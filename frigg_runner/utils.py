# -*- coding: utf8 -*-

import sys
import time

import click


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
            click.secho('Build success', fg='green')
            exit(0)
        else:
            click.secho('Build fail', fg='red')
            exit(1)


def newline():
    click.echo('', nl=True)


def put_task_result(task_result, color, setup=False):
    click.secho('  # %s (%s%s) %s' % (task_result.task, round(task_result.time, ndigits=2), 's',
                                      ('(setup task)' if setup else '')), fg=color)


def print_task(task):
    if task:
        return ':  %s' % task
    else:
        return ''
