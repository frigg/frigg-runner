# -*- coding: utf8 -*-
import os

import frigg_coverage
import invoke
from clint.textui import colored, indent, progress, puts, puts_err
from frigg import projects
from invoke.exceptions import Failure
from invoke.runner import Result

from . import __name__, __version__
from .utils import exit_build, newline, put_task_result, timeit


class Runner(object):

    def __init__(self, failfast, verbose, path=None):
        """
        Initialize the local build

        :param failfast: Stop build then a task exit with a code other than 0
        :param verbose: Print task output directly to stdout and stderr
        """
        self.fail_fast = failfast
        self.verbose = verbose
        self.directory = path or os.getcwd()

        puts(colored.blue('%s %s' % (__name__, __version__), bold=True))
        puts('Path: %s' % self.directory)
        newline()

        if not os.path.exists(self.directory):
            puts(colored.red('The given working directory does not exist'))
            exit_build(False)

        try:
            self.config = projects.build_settings(self.directory)
        except RuntimeError:
            puts(colored.red('No tasks found!'))
            exit_build(True)

    def coverage(self):
        """
        Check test coverage. Print coverage if coverage information exist in frigg configuration
        """
        try:
            if self.config.get('coverage', False):
                coverage = frigg_coverage.parse_coverage(
                    os.path.join(self.directory, self.config['coverage']['path']),
                    self.config['coverage']['parser']
                )
                puts(colored.blue('Coverage %s%s' % (round(coverage, ndigits=2), '%')))
        except (KeyError, TypeError):
            pass

    @timeit
    def run_task(self, command):
        """
        Run a task and return a task result
        Print output based on the --verbose parameter

        :param command: The command to execute
        :return: (Result) Invoke task result
        """
        try:
            if self.verbose:
                puts(colored.yellow(self.directory, command))
            result = invoke.run('cd %s && %s' % (self.directory, command),
                                hide=(bool(not self.verbose) or None))
            return result
        except Failure as failure:
            return failure.result
        except SystemExit:
            pass
        return None

    def run(self):
        """
        Run all tasks
        """
        tasks = self.config['tasks']

        # List all tasks
        puts(colored.yellow('Tasks'))
        with indent(quote='#', indent=2):
            for task in tasks:
                puts(colored.yellow(task))
        newline()

        task_results = []
        with progress.Bar(label="Running tasks ", expected_size=len(tasks), width=60) as bar:
            for task in tasks:
                task_index = tasks.index(task)
                task_time, task_result = self.run_task(task)
                task_result.task = task
                task_result.time = task_time
                if isinstance(task_result, Result):
                    task_results.append(task_result)
                bar.show(task_index+1)

                # Fail fast
                if task_result.failed and self.fail_fast:
                    if not self.verbose:
                        puts(colored.red(task_result.task))
                        puts(task_result.stdout)
                        puts_err(task_result.stderr)
                    exit_build(False)

        newline()
        self.handle_results(task_results)

    def handle_results(self, task_results):

        # Create a list of all failures
        failures = []
        for task_result in task_results:
            if task_result.failed:
                failures.append(task_result)

        # Print output from failed tasks, drop it if the runner is in verbose mode.
        if len(failures) > 0 and not self.verbose:
            puts(colored.red('Failures'))
            for task_result in failures:
                with indent(quote='#', indent=2):
                    put_task_result(task_result, colored.red)
                puts(task_result.stdout)
                puts_err(task_result.stderr)
            newline()

        # Print the overall build result
        puts(colored.blue('Result'))
        with indent(quote='#', indent=2):
            for task_result in task_results:
                if task_result.failed:
                    put_task_result(task_result, colored.red)
                elif task_result.ok:
                    put_task_result(task_result, colored.green)

        newline()

        # Print build time
        puts(colored.blue('Total runtime: %ss' % round(sum(map(lambda task: task.time,
                                                               task_results)), ndigits=2)))

        # Print coverage
        self.coverage()

        # Exit build with a message and a exit code
        exit_build(bool(len(failures) == 0))
