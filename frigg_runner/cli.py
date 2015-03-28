# -*- coding: utf-8 -*-

import click

from frigg_runner.runner import Runner


@click.command()
@click.option('-f', '--failfast', is_flag=True, default=False,
              help='Don\'t exit if one of the tasks returns other than statuscode 0.')
def main(**kwargs):
    Runner(**kwargs).run()


if __name__ == '__main__':
    main()
