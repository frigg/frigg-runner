from abc import abstractmethod


class BaseTaskRunner(object):

    def __init__(self, verbose, directory):
        self.verbose = verbose
        self.directory = directory

    @property
    @abstractmethod
    def name(self):
        raise NotImplementedError

    def initialize(self):
        yield None

    def execute_task(self, task):
        pass
