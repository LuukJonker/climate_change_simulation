from math import pi, cos


class World(object):
    def __init__(self, data, wsd):
        """
        Creates a world with a average temperature. Local temperatures are found in coordinates.
        :data = a dictionary with all the necessary instances.
        :wsd (World Specific Data) = a dictionary containing the radius and power.
        """

        self.time = data['time']
        self.ghg = data['ghg']
        self.albedo = data['albedo']
        self.countries = data['countries']
        self.coordinates = data['coordinates']
        self.angle = 0.39795 * cos(0.98563 * (self.time.total_days - 173))
        self.radius = wsd['radius']  # In metres
        self.surface = pi * self.radius**2
        self.globe = 4 * pi * self.radius**2
        self.PowerIn = wsd['wattPerSquareMetre'] * self.surface
        self.EnergyIn = self.PowerIn - self.PowerIn * self.albedo.albedo
        self.temperature = 13.5  # Temp in Celsius
        self.ground_temperature = 13.5

    @staticmethod
    def get_average(li):
        return sum(li) / len(li)

    def update(self):
        self.angle = 0.39795 * cos(0.98563 * (self.time.total_days - 173))

        self.ghg.update(self.time.decimal_time)

        temp, ground_temp, albedo, ghg, snow, land_albedo, cloud_albedo, absorption = [], [], [], [], [], [], [], []

        for x in self.coordinates:
            for y in x:
                y.update(self.temperature)
                ground_temp.append(y.temp_ground)
                temp.append(y.temperature)
                albedo.append(y.albedo.albedo)
                snow.append(y.albedo.snow_coverage)
                land_albedo.append(y.albedo.ground_albedo)
                cloud_albedo.append(y.albedo.cloud_albedo)
                ghg.append(y.ghg.total_ppm)
                absorption.append(y.ghg.absorption)
        self.temperature = self.get_average(temp)
        self.ground_temperature = self.get_average(ground_temp)
        self.albedo.albedo = self.get_average(albedo)
        self.albedo.snow_coverage = self.get_average(snow)
        self.albedo.ground_albedo = self.get_average(land_albedo)
        self.albedo.cloud_albedo = self.get_average(cloud_albedo)
