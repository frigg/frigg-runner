# -*- coding: utf8 -*-

import os.path

DEFAULT_CONFIG_FILES = ['.frigg.yml', '.frigg.yaml']


class Runner(object):

    def __init__(self, config_file, full_run):
        self.config_file = config_file
        self.full_run = full_run

    def run(self):
        pass

    def get_config_file_name(self):
        if self.config_file:
            if os.path.isfile(self.config_file):
                return self.config_file
        else:
            for file in DEFAULT_CONFIG_FILES:
                if os.path.isfile(file):
                    return file
        return None
