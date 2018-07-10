from time import time


class Timer(object):

    def __init__(self):
        self.reset()


    def start(self):
        self.starting_time = time()


    def stop(self, reset=False):
        if self.starting_time:
            self.ending_time = time()
            time_difference = int(self.ending_time - self.starting_time)
            minutes = int(time_difference / 60)
            seconds = time_difference % 60

            if reset:
                self.reset()
                
            return minutes, seconds


    def reset(self):
        self.starting_time = None
        self.ending_time = None
