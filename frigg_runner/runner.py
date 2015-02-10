# -*- coding: utf8 -*-

import os
import sys

from frigg.projects import build_settings
from invoke import run as cmd_run
from invoke.exceptions import Failure

from . import __name__, __version__

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
FAIL = '\033[91m'
ENDC = '\033[0m'


class Runner(object):

    def __init__(self, fail_fast):
        self.fail_fast = fail_fast
        self.directory = os.getcwd()
        try:
            self.config = build_settings(self.directory)
        except RuntimeError:
            print('No tasks found in %s' % self.directory)

    def run(self):
        self.print_welcome()

        self.print_info_line('', color=OKBLUE)
        self.print_info_line('Detected tasks:', color=OKBLUE)
        tasks = self.config['tasks']
        for task in tasks:
            self.print_info_line('* %s' % task, color=OKBLUE)
        self.print_hash_line(color=OKBLUE)

        print('')

        status = {
            'success': [],
            'failure': []
        }

        for task in tasks:
            task_result = self.run_task(task)
            if task_result:
                status['success'].append(task)
            else:
                status['failure'].append(task)

            print('\n\n')

        self.print_status(status)

    def run_task(self, command):
        self.print_hash_line(color=HEADER)
        self.print_info_line(command, color=HEADER)
        self.print_hash_line(color=HEADER)

        try:
            print('')
            cmd_run(command)
        except (SystemExit, Failure):

            self.print_hash_line(color=FAIL)
            self.print_info_line('%s exited with a statuscode other than 0' % command, color=FAIL)
            self.print_hash_line(color=FAIL)

            if self.fail_fast:
                sys.exit(1)

            return False

        return True

    def print_welcome(self):
        self.print_hash_line(color=OKBLUE)
        self.print_info_line('%s %s' % (__name__, __version__), color=OKBLUE)

    def print_hash_line(self, color=None):
        prefix = ''
        end = ''
        if color:
            prefix = color
            end = ENDC
        print(prefix + ''.join(['#' for x in range(self.get_console_with())]) + end)

    def print_info_line(self, content, color=None):
        prefix = ''
        end = ''
        if color:
            prefix = color
            end = ENDC
        first = '# %s' % content
        print(prefix + first.ljust((self.get_console_with()) - 1) + '#' + end)

    def get_console_with(self):
        try:
            rows, columns = os.popen('stty size', 'r').read().split()
            return int(columns)
        except:
            return 79

    def print_status(self, status):
        if len(status['failure']) > 0:
            self.print_hash_line(color=FAIL)
            self.print_info_line('Build / Tests failure', color=FAIL)
            self.print_info_line('The following tasks ended with a exitcode other than 0',
                                 color=FAIL)
            for task in status['failure']:
                self.print_info_line('* %s' % task, color=FAIL)
            self.print_hash_line(color=FAIL)

        else:
            self.print_hash_line(color=OKGREEN)
            self.print_info_line('Build success!', color=OKGREEN)
            self.print_hash_line(color=OKGREEN)
