# -*- coding: utf-8 -*-

import click

from frigg_runner.runner import Runner


@click.command()
@click.option('-f', '--failfast', is_flag=True, default=False,
              help='Exit if one of the tasks returns other than statuscode 0.')
@click.option('-v', '--verbose', is_flag=True, default=False, help='Print output from every task.')
def main(**kwargs):
    Runner(**kwargs).run()


if __name__ == '__main__':
    main()
