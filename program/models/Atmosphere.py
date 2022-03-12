from math import log


class GHG(object):
    def __init__(self):
        self.total_ppm = 400
        self.emissions = 0
        self.absorption = 0.78
        self.options = [lambda p: 0.73 + 3.9 * 10 ** -7 * p ** 2, lambda p: 0.69 + 2.5 * 10 ** -4 * p,
                        lambda p: 0.31 + 8.0 * 10 ** -2 * log(p), lambda p: -0.14 + p / (p + 31)]

        self.trends = [(578.9682337, 21570.51725543)]

        self.trend = lambda t: 578.9682337 * t + -1.13057627 * 10 ** 6

    def calculate_absorption(self, time, option=2):
        #if time >= 2020:
        #    self.trend = lambda t: (578.9682337 * t + -1.13057627 * 10 ** 6) * 0.946**(t - 2020)
        self.emissions = self.trend(time)
        self.total_ppm += self.emissions / 17_300
        self.absorption = self.options[option](self.total_ppm)

    def update(self, time):
        self.calculate_absorption(time)
