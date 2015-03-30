# -*- coding: utf-8 -*-

import click

from frigg_runner.runner import Runner


@click.command()
@click.option('-f', '--failfast', is_flag=True, default=False,
              help='Exit if one of the tasks returns other than statuscode 0.')
@click.option('-v', '--verbose', is_flag=True, default=False, help='Print output from every task.')
@click.option('-p', '--path', default=None, help='Working directory, the path where the '
                                                 'friggfile lives.')
def main(**kwargs):
    Runner(**kwargs).run()


if __name__ == '__main__':
    main()
