# -*- coding: utf8 -*-
import os

import click
import frigg_coverage
import frigg_settings
import invoke
from invoke.exceptions import Failure
from invoke.runner import Result
from yaml import parser, scanner

from . import __name__, __version__
from .utils import exit_build, newline, print_task, put_task_result, timeit

runner_wrapper = frigg_settings.FileSystemWrapper()


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
            self.config = frigg_settings.build_settings(self.directory, runner_wrapper)
        except RuntimeError:
            click.secho('No tasks found!', fg='red')
            exit_build(True)
        except (parser.ParserError, scanner.ScannerError, TypeError) as exception:
            click.secho('Could not read frigg file: %s' % str(exception), fg='red')
            exit_build(False)

    def coverage(self):
        """
        Check test coverage. Print coverage if coverage information exist in frigg configuration
        """
        try:

            if self.config.get('coverage', False):
                coverage_file = os.path.join(self.directory, self.config['coverage']['path'])
                parser = self.config['coverage']['parser']
                coverage_report = None

                if os.path.exists(coverage_file):
                    with open(coverage_file, 'r') as file:
                        coverage_report = file.read()

                coverage = frigg_coverage.parse_coverage(coverage_report, parser)

                click.secho('Coverage %s%s' % (round(coverage, ndigits=2), '%'), fg='blue')

        except (KeyError, TypeError, OSError) as exception:
            click.secho('Unable to parse the coverage report.', fg='red')
            click.secho(str(exception), fg='red')
            return exit_build(False)

    @timeit
    def run_task(self, command):
        """
        Run a task and return a task result

        :param command: The command to execute
        :return: (Result) Invoke task result
        """
        try:
            if self.verbose:
                newline()
            result = invoke.run('cd %s && %s' % (self.directory, command),
                                hide=(bool(not self.verbose) or None), encoding='utf8')
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
        with click.progressbar(tasks, label='Running tasks', show_eta=False,
                               item_show_func=print_task) as bar:
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
