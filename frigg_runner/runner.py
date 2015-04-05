# -*- coding: utf8 -*-
import os

import click
import frigg_coverage
import invoke
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

        click.secho('%s %s' % (__name__, __version__), fg='blue', bold=True)
        click.echo('Path: %s' % click.format_filename(self.directory))
        newline()

        if not os.path.exists(self.directory):
            click.secho('The given working directory does not exist', fg='red')
            exit_build(False)

        try:
            self.config = projects.build_settings(self.directory)
        except RuntimeError:
            click.secho('No tasks found!', fg='red')
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
                click.secho('Coverage %s%s' % (round(coverage, ndigits=2), '%'), fg='blue')
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
                click.secho(' - %s ' % command, fg='yellow')
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
        click.secho('Tasks', fg='yellow')
        for task in tasks:
            click.secho('  # %s' % task, fg='yellow')
        newline()

        task_results = []
        with click.progressbar(tasks, label='Running tasks', show_eta=False) as bar:
            for task in bar:
                task_time, task_result = self.run_task(task)
                task_result.task = task
                task_result.time = task_time
                if isinstance(task_result, Result):
                    task_results.append(task_result)

                # Fail fast
                if task_result.failed and self.fail_fast:
                    if not self.verbose:
                        click.secho(task_result.task, fg='red')
                        click.echo(task_result.stdout)
                        click.echo(task_result.stderr, err=True)
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
            click.secho('Failures', fg='red')
            for task_result in failures:
                put_task_result(task_result, 'red')

                click.echo(task_result.stdout)
                click.echo(task_result.stderr, err=True)
            newline()

        # Print the overall build result
        click.secho('Result', fg='blue')
        for task_result in task_results:
            if task_result.failed:
                put_task_result(task_result, 'red')
            elif task_result.ok:
                put_task_result(task_result, 'green')

        newline()

        # Print build time
        click.secho('Total runtime: %ss' %
                    round(sum(map(lambda task: task.time, task_results)), ndigits=2), fg='blue')

        # Print coverage
        self.coverage()

        # Exit build with a message and a exit code
        exit_build(bool(len(failures) == 0))
