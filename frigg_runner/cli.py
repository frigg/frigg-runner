# -*- coding: utf-8 -*-

from optparse import OptionParser

from frigg_runner.runner import Runner


def main():

    parser = OptionParser()

    parser.add_option('-f', '--failfast', action='store_true', dest='fail_fast', default=False,
                      help='Don\'t exit if one of the tasks returns other than statuscode 0.')

    (options, args) = parser.parse_args()

    runner = Runner(fail_fast=options.fail_fast)
    runner.run()

if __name__ == '__main__':
    main()
