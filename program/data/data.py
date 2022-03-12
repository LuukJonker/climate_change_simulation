import csv
import sys
import os
from json import load
import numpy as np

from PIL import Image
from imutils import paths
from collections import Counter


class Data:
    def __init__(self, BASEPATH, logging):
        self.BASEPATH = BASEPATH
        self.logging = logging
        self.climate_map_path = os.path.join(BASEPATH, "data/country/")
        self.climate_map = Image.open(os.path.join(self.BASEPATH,
                                                   r'data/climate/img/climate_map.png'))  # 3927 x 1947 pixels
        self.img_array = self.climate_map.load()
        self.step = 5

        self.climate_color_hashmap = {
            (255, 255, 255): 'ocean',
            (0, 125, 125): 'dfc',
            (0, 120, 255): 'am',
            (102, 102, 102): 'ef',
            (178, 178, 178): 'et',
            (0, 70, 95): 'dfc',
            (15, 117, 127): 'dfc',
            (150, 50, 150): 'dsc',
            (134, 57, 147): 'dsc',
            (153, 64, 153): 'dsc',
            (118, 118, 118): 'et',
            (255, 220, 100): 'bsk',
            (209, 36, 183): 'dsc',
            (255, 150, 150): 'bwk',
            (255, 0, 0): 'bwh',
            (149, 254, 149): 'cwa',
            (0, 255, 255): 'dfa',
            (200, 255, 80): 'cfa',
            (55, 200, 255): 'dfb',
            (70, 170, 250): 'aw',
            (0, 0, 255): 'af',
            (100, 255, 80): 'cfb',
            (255, 255, 0): 'csa',
            (133, 170, 54): 'cfb',
            (150, 255, 150): 'cfa',
            (245, 165, 0): 'bsh',
            (75, 80, 179): 'dwc',
            (170, 175, 255): 'dwa',
            (50, 0, 135): 'dwd',
            (89, 120, 220): 'dwb',
        }


    def get_data(self, name):
        data = {
            'csv': self.get_csv_data_with_country_name(name),
            'location': self.get_location_with_country_name(name),
        }
        return data

    def get_country_with_location(self):
        with open(os.path.join(self.BASEPATH, 'data/country/country.json')) as json_file:
            return load(json_file)

    def get_country_names(self):
        names = []
        with open(os.path.join(self.BASEPATH, 'data/country/csv/GHG_emissions.csv'), 'r') as csv_file:
            contents = list(csv.reader(csv_file))
            for country in contents:
                names.append(country[0])
        return names

    def get_csv_data_with_country_name(self, name):
        data = {}
        for index, file in enumerate(files := list(paths.list_files(os.path.join(self.BASEPATH, 'data/country/csv')))):
            sys.stdout.write(f"\rLoading in csv file {index + 1} out of {len(files)}")
            sys.stdout.flush()
            sys.stdout.write("\n")
            # Make a list of all the paths in the csv directory
            with open(file, 'r') as csv_file:  # Open the files
                contents = list(csv.reader(csv_file))  # Read the contents and make a 3d list out of it
                data[os.path.splitext(os.path.basename(csv_file.name))[
                    0]] = None  # Set data of to None incase nothing is found
                for country in contents:  # Go over all countries in the csv file
                    if country[0].lower() == name.lower():  # Check if it is the right country, otherwise continue
                        amount_with_year = {}  # Create empty dictionary
                        for country_index, amount in enumerate(country[1:]):
                            # Go over all the data for the country with index
                            amount_with_year[contents[0][country_index + 1]] = amount  # Link the year to the data
                        data[os.path.splitext(os.path.basename(csv_file.name))[
                            0]] = amount_with_year  # Put it all in the dictionary under the name of the csv file
        return data

    def get_location_with_country_name(self, name):
        with open(os.path.join(self.BASEPATH, 'data/country/country.json')) as json_file:
            try:
                return load(json_file)[name]
            except KeyError:
                return None

    def get_climate_with_coordinates(self, coordinates, area):
        n = self.step
        colors = []
        x_reach, y_reach = area  # (width, height)
        for x in range(coordinates[0] + int(x_reach / n),
                       coordinates[0] + x_reach, int(x_reach / n)):
            for y in range(coordinates[1] + int(y_reach / n),
                           coordinates[1] + y_reach, int(y_reach / n)):
                colors.append(self.convert_rgba_to_rgb(self.img_array[int(x * 3927 / 360), int(y * 1947 / 180)]))
        sorted_colors = list(dict.fromkeys([item for items, c in Counter(colors).most_common()
                                            for item in [items] * c]))
        try:
            return self.climate_color_hashmap[sorted_colors[0] if sorted_colors[0] != (0, 0, 0) else sorted_colors[1]]
        except KeyError:
            return 'ocean'

    @staticmethod
    def convert_rgba_to_rgb(rgba):
        alpha = int(rgba[3] / 255)
        print(alpha) if alpha != 1 else ''

        return (
            int(rgba[0] * alpha),
            int(rgba[1] * alpha),
            int(rgba[2] * alpha)
        )
