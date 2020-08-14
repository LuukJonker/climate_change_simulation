from imutils import paths
from json import load

import csv
import os


class Data:
    def __init__(self, BASEPATH):
        self.BASEPATH = BASEPATH

    def get_data(self, name):
        data = {
            'csv': self.get_csv_data_with_country_name(name),
            'location': self.get_location_with_country_name(name),
            }
        return data

    def get_country_names(self):
        names = []
        with open(os.path.join(self.BASEPATH, 'data/country/csv/GHG_emissions.csv'), 'r') as csv_file:
            contents = list(csv.reader(csv_file))
            for country in contents:
                names.append(country[0])
        return names

    def get_csv_data_with_country_name(self, name):
        data = {}
        for file in list(paths.list_files(os.path.join(self.BASEPATH, 'data/country/csv'))):
            # Make a list of all the paths in the csv directory
            with open(file, 'r') as csv_file:  # Open the files
                contents = list(csv.reader(csv_file))  # Read the contents and make a 3d list out of it
                data[os.path.splitext(os.path.basename(csv_file.name))[
                    0]] = None  # Set data of to None incase nothing is found
                for country in contents:  # Go over all countries in the csv file
                    if country[0].lower() == name.lower():  # Check if it is the right country, otherwise continue
                        amount_with_year = {}  # Create empty dictionary
                        for index, amount in enumerate(country[1:]):  # Go over all the data for the country with index
                            amount_with_year[contents[0][index + 1]] = amount  # Link the year to the data
                        data[os.path.splitext(os.path.basename(csv_file.name))[
                            0]] = amount_with_year  # Put it all in the dictionary under the name of the csv file
        return data

    def get_location_with_country_name(self, name):
        with open(os.path.join(self.BASEPATH, 'data/country/country.json')) as json_file:
            try:
                return load(json_file)[name]
            except KeyError:
                return None
