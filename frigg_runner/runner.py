# -*- coding: utf8 -*-

DEFAULT_CONFIG_FILES = ['.frigg.yml', '.frigg.yaml']


class Runner(object):

    def __init__(self, config_file, full_run):
        self.config_file = config_file
        self.full_run = full_run

    def run(self):
        pass
