from math import exp

SNOW_ALBEDO = 0.8
CLOUD_COVERAGE = 0.4

DROPLET_SIZE = 0.000029
SEA_DIFFERENCE = 5


class Albedo(object):
    def __init__(self, climate=None):
        self.albedo = .33
        self.ground_albedo = .12
        self.cloud_albedo = .54

        self.snow_coverage = 0

        self.average_albedo_earth = {
            'o': .07,
            'e': .22,
            'b': .13,
            'a': .05,
            'c': .09,
            'd': .06,
        }

        self.local_climate = climate

    def cloud_albedo_generator(self, temperature):
        water_quantity = 54 * 10 ** -3 * exp(0.05 * temperature)
        droplet_size = DROPLET_SIZE if self.local_climate[0] == 'o' else DROPLET_SIZE / SEA_DIFFERENCE
        return water_quantity/(water_quantity + 4.47 * 10 ** 3 * droplet_size)

    def snow_generator(self, temperature):
        self.snow_coverage = 1 if temperature <= -40 else 1 - 0.00033 * (temperature + 40) ** 2 \
            if -40 < temperature <= 15 else 0

    def calculate_albedo(self):
        if self.local_climate[0] in self.average_albedo_earth.keys():
            return self.average_albedo_earth[self.local_climate[0]]
        else:
            return 0

    def update(self, temperature):
        self.ground_albedo = self.calculate_albedo()
        if self.local_climate[0] != 'o':
            self.snow_generator(temperature)
            self.ground_albedo = (self.snow_coverage * SNOW_ALBEDO + (1 - self.snow_coverage) * self.ground_albedo + self.ground_albedo) / 2
        self.cloud_albedo = self.cloud_albedo_generator(temperature) * CLOUD_COVERAGE
        self.albedo = 1 - ((1 - self.cloud_albedo) * (1 - self.ground_albedo))
        #self.albedo = CLOUD_COVERAGE * self.cloud_albedo + (1 - CLOUD_COVERAGE) * self.ground_albedo
