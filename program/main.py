try:
    from models.World import World
    from models.Albedo import Albedo
    from models.GHG import GHG
    from models.Country import Country
    from models.Coordinates import Coordinates
    from models.Time import Time
    from data.data import Data

    from mapping.mapping import Mapping
    from mapping.logging import Logging

except ModuleNotFoundError:
    from program.models.World import World
    from program.models.Albedo import Albedo
    from program.models.GHG import GHG
    from program.models.Country import Country
    from program.models.Coordinates import Coordinates
    from program.models.Time import Time
    from program.data.data import Data

    from program.mapping.mapping import Mapping
    from program.mapping.logging import Logging

from pathlib import Path

from sys import stdout, exit

BASEPATH = Path(__file__).parent.absolute()


def create_list_coordinates(interval, instances):
    x_interval, y_interval = int(360 / interval), int(
        180 / interval)  # Get the exact amount of x and y coordinates in the list
    coordinates_list = [[None] * y_interval] * x_interval  # Create a 2d list with Nonetypes in the shape of the
    # coordinate list
    for x, x_value in enumerate(coordinates_list):  # x is the position and x_value is the list containing the y values
        for y, _ in enumerate(x_value):  # Loop over the y values for every x
            coordinates_list[x][y] = Coordinates((x * x_interval, y * y_interval),
                                                 (1731000 / 36, 1731000 / 18), instances)
            # Change the value to a instance of the coordinate class
            stdout.write(f"\rCreated coordinate ({x},{y}). { y + x * len(x_value) }")
            stdout.flush()
            stdout.write("\n")
    return coordinates_list


def setup(coordinates_interval):
    logging = Logging(BASEPATH)  # Create an instance of the logging


    logging.log_event('Starting the setup', 'main')  # Log the start up to the loggin file

    data_instance = Data(BASEPATH, logging)

    wsd = {'radius': 6371000, 'wattPerSquareMetre': 1368}

    data = dict(time=Time(), albedo=Albedo(BASEPATH),
                countries=[Country(c, data_instance.get_data(c)) for c in data_instance.get_country_names()],
                coordinates=create_list_coordinates(coordinates_interval, {
                    'albedo': Albedo,
                    'ghg': GHG,
                                                                           }))
    print('got here')
    earth = World(data, wsd)

    variable_names = {
        'earth': list(earth.__dict__.keys()),
    }

    mapping = Mapping(BASEPATH, logging, variable_names)

    return earth, data['time'], mapping


def handler(length, earth, time, mapping):
    for t in range(length):
        time.proceed()
        mapping.values[t] = vars(earth)
        print(t)
    print('hello')
    #mapping.save_csv()


def main():
    earth, time, mapping = setup(10)
    handler(10, earth, time, mapping)
    return earth


if __name__ == '__main__':
    main()
