import sys
from os.path import join
from datetime import datetime


class Logging:
    def __init__(self, BASEPATH):
        self.BASEPATH = BASEPATH

        self.log_file = open(join(self.BASEPATH, 'mapping/log.txt'), 'w')

    def log_event(self, event, orgin):
        self.log_file.write(f"[{ self.time() }] { orgin }: { event }")

    def log_error(self, error, orgin):
        self.log_file.write(f"[ERROR] [{ self.time() }] { orgin }: { error }")

    @staticmethod
    def time():  # Returns the time in a form of a string
        return datetime.now().strftime("%H:%M:%S")

    @staticmethod
    def loop_print(string):
        sys.stdout.write(f'\r{string}')
        sys.stdout.flush()
