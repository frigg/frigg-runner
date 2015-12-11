# -*- coding: utf8 -*-
import os

import click
import frigg_settings
from yaml import parser, scanner

from frigg_runner.constants import BLUE_COLOR
from frigg_runner.utils import error, exit, write_output

from . import __name__, __version__

runner_wrapper = frigg_settings.FileSystemWrapper()


class Runner(object):

    def __init__(self, failfast=False, verbose=False, setup=False, path=None):
        """
        Initialize the local build

        :param failfast: Stop build then a task exit with a code other than 0
        :param verbose: Print task output directly to stdout and stderr
        :param setup: Run setup tasks before test tasks
        :param path: Frigg runner working directory
        """
        self.fail_fast = failfast
        self.verbose = verbose
        self.setup = setup
        self.directory = path or os.getcwd()

        if not os.path.exists(self.directory):
            error('The given working directory does not exist')
            exit(1)
        try:
            self.config = frigg_settings.build_settings(self.directory, runner_wrapper)
        except RuntimeError:
            error('No tasks found!')
            exit(1)
        except (parser.ParserError, scanner.ScannerError, TypeError) as exception:
            error('Could not read frigg file', exception)
            exit(1)

        # We currently only support the local filesystem runner, a simple import is done here.
        # We may support other backends later, maybe docker or remote frigg.

        from .runners import local_task_runner
        self.runner = local_task_runner.LocalTaskRunner(
            verbose=self.verbose,
            directory=self.directory,
        )

    def run(self):
        self.bootstrap()
        self.setup_tasks()
        self.tasks()
        self.verbose_tasks()
        self.result()

    def bootstrap(self):
        write_output('{name} {version}\nPath: {cwd}\nRunner: {runner}'.format(
            name=__name__,
            version=__version__,
            cwd=click.format_filename(self.directory),
            runner=self.runner.name
        ), color=BLUE_COLOR)

        with click.progressbar(self.runner.initialize(), label='Initializing task runner...') \
                as bar:
            try:
                list(bar)
            except Exception as exception:
                error('Could not initialize the task runner', exception)

    def setup_tasks(self):
        setup_tasks = self.config.get('setup_tasks', None)
        if self.setup and setup_tasks:
            print(setup_tasks)

    def tasks(self):
        tasks = self.config.get('tasks', [])
        print(tasks)

    def verbose_tasks(self):
        verbose_tasks = self.config.get('verbose_tasks', None)
        if not self.verbose and verbose_tasks:
            print(verbose_tasks)

    def result(self):
        pass
