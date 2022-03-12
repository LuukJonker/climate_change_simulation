from math import sin, cos, radians
import requests
import pandas as pd

class Coordinates(object):
    def __init__(self, coordinates, interval, area, climate, data):
        self.countries = None
        self.coordinates = coordinates
        self.r_coordinates = (coordinates[0] - 180, coordinates[1] - 90)
        self.interval = interval
        self.angle = cos(coordinates[1])
        self.area = area  # (height, width)
        # self.altitude = self.get_altitude_with_coordinates()
        self.climate = climate  # 'climate'
        self.ghg = data['ghg']
        self.albedo = data['albedo'](self.climate)
        self.temperature = 13.5
        self.temp_ground = 13.5
        self.temp_atmosphere = 0
        self.get_country_with_coordinates(data['country_names'],  # {'country': [long, lat]}
                                          data['country_instances'])
        self.solar_constant = 1_360  # Watt per square meter in vacuum
        self.power_returned = 0

        self.world_instance = None

    def get_country_with_coordinates(self, names, instances):
        country_list = []
        x_reach, y_reach = 360 / self.interval, 180 / self.interval
        for country in names.items():  # ('country': [long, lat])
            if self.r_coordinates[0] + x_reach > country[1][0] > self.r_coordinates[0]:
                if self.r_coordinates[1] + y_reach > country[1][1] > self.r_coordinates[1]:
                    for c in instances:
                        if c.name == country[0]:
                            country_list.append(c)

        self.countries = country_list
        self.ghg.ghg = sum([float(country.ghg) for country in self.countries])

    def get_altitude_with_coordinates(self):
        query = ('https://api.open-elevation.com/api/v1/lookup'
                 f'?locations={self.coordinates[0]}{self.coordinates[1]}')
        r = requests.get(query).json()  # Creates a json object
        return pd.json_normalize(r, 'results')['elevation'].values[0]  # Use pandas to
        # get the elevation out of the json object

    def calculate_current_temperature(self):
        power_sun = abs(sin(radians(self.coordinates[1] + self.world_instance.angle))) * \
                    self.area[0] * self.area[1] * self.solar_constant / 2
        power_incoming = power_sun + self.power_returned
        power_absorbed = power_incoming * (1 - self.albedo.albedo)
        self.temp_ground = (power_absorbed / (5.670373 * 10 ** -8 * self.area[0] * self.area[1])) ** 0.25 - 273.15
        power_radiated = power_absorbed
        self.power_returned = power_radiated * self.albedo.cloud_albedo
        power_atmosphere = self.ghg.absorption * power_radiated * (1 - self.albedo.cloud_albedo)
        self.temp_atmosphere = (power_atmosphere / (
                    5.670373 * 10 ** -8 * self.area[0] * self.area[1] * self.ghg.absorption)) ** 0.25 - 273.15
        self.power_returned += power_atmosphere / 2

    def equalize(self, average_temp):
        self.temperature = (average_temp - self.temp_ground) * 0.75 + self.temp_ground

    def update(self, average_temp):
        self.albedo.update(self.temperature)
        self.ghg.ghg = sum([float(country.ghg) for country in self.countries])

        self.calculate_current_temperature()
        self.equalize(average_temp)
