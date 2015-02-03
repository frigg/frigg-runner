# -*- coding: utf-8 -*-

from optparse import OptionParser

from frigg_runner.runner import Runner
from frigg_runner.startup import welcome_message


def main():

    print(welcome_message() + '\n')

    parser = OptionParser()

    parser.add_option('-c', '--config', dest='config_file', help='The relative path to frigg '
                                                                 'config file.')
    parser.add_option('-f', '--full', action='store_true', dest='full_run', default=False,
                      help='Don\'t exit if one of the tasks returns other than statuscode 0.')

    (options, args) = parser.parse_args()

    runner = Runner(config_file=options.config_file, full_run=options.full_run)
    runner.run()

if __name__ == '__main__':
    main()
