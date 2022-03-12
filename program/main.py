try:
    from models.World import World
    from models.Albedo import Albedo
    from models.Atmosphere import GHG
    from models.Country import Country
    from models.Coordinates import Coordinates
    from models.Time import Time
    from data.data import Data

    from mapping.mapping import Mapping
    from mapping.logging import Logging

except ModuleNotFoundError:
    from program.models.World import World
    from program.models.Albedo import Albedo
    from program.models.Atmosphere import GHG
    from program.models.Country import Country
    from program.models.Coordinates import Coordinates
    from program.models.Time import Time
    from program.data.data import Data

    from program.mapping.mapping import Mapping
    from program.mapping.log import Logging

from pathlib import Path

from json import load as json_load
from os.path import join as path_join
from os import getpid
from psutil import Process

BASEPATH = Path(__file__).parent.absolute()

logging = Logging(BASEPATH)  # Create an instance of the logging
data_instance = Data(BASEPATH, logging)


def create_list_coordinates(interval, instances):
    x_interval, y_interval = int(360 / interval), int(180 / interval)
    coordinates_list = []
    for x in range(x_interval):
        new_list = []
        for y in range(y_interval):
            new_list.append(Coordinates(coords := (x * interval, y * interval), interval, (1731000 / 36, 1731000 / 18),
                                        data_instance.get_climate_with_coordinates(coords, (interval, interval)),
                                        instances))
           # stdout.write(f"\rCreated coordinate ({x},{y}). {x_interval * y_interval}")
           # stdout.flush()
        coordinates_list.append(new_list)
    #stdout.write('\n')
    return coordinates_list


def save_values(t, world, mapping):
    coordinates_list = []
    for x in world.coordinates:
        new_list = []
        for y in x:
            new_list.append([y.temp_ground, y.albedo.albedo, y.climate])
        coordinates_list.append(new_list)
    mapping.values[t] = {
        'time': world.time.decimal_time,
        'temp': world.temperature,
        'ground': world.ground_temperature,
        'albedo': world.albedo.albedo,
        'ground_albedo': world.albedo.ground_albedo,
        'co2_in_atmosphere': world.ghg.total_ppm,
        'absorption': world.ghg.absorption,
        'cloud': world.albedo.cloud_albedo,
        'snow': world.albedo.snow_coverage,
        'coordinates': coordinates_list,
    }
    temps = [y.temperature for x in world.coordinates for y in x]
    mapping.max_temp = max(mapping.max_temp, max(temps))
    mapping.min_temp = min(mapping.min_temp, min(temps))


def setup(coordinates_interval):
    with open(path_join(BASEPATH, 'input/input.json')) as json_file:
        settings = json_load(json_file)

    logging.log_event('Starting the setup', 'main')  # Log the start up to the loggin file

    wsd = {'radius': 6371000, 'wattPerSquareMetre': 1368}

    country_list = [Country(c, GHG, data_instance.get_data(c)) for c in data_instance.get_country_names()]

    ghg_instance = GHG()

    data = dict(time=Time(settings['start_year']), albedo=Albedo(), ghg=ghg_instance,
                countries=country_list,
                coordinates=create_list_coordinates(coordinates_interval, {
                    'albedo': Albedo,
                    'ghg': ghg_instance,
                    'country_names': data_instance.get_country_with_location(),  # {'country': [long, lat], ...}
                    'country_instances': country_list,
                }))

    earth = World(data, wsd)

    for c_x in earth.coordinates:
        for c_y in c_x:
            c_y.world_instance = earth
            c_y.calculate_current_temperature()

    mapping = Mapping(BASEPATH, settings['start_year'], data['time'].time_interval)

    return earth, data['time'], mapping


def handler(years, earth, time, mapping):
    num = (years + 10) * time.options[time.time_interval]
    for t in range(num):
        time.proceed()
        earth.update()
        save_values(t, earth, mapping)
    mapping.save()


def display_current_memory_usage():
    process = Process(getpid())
    return f'{ process.memory_info().rss / 1024 / 1024 } mb'


def main():
    num_of_years = 10
    earth, time, mapping = setup(10)
    handler(num_of_years, earth, time, mapping)
    return earth, mapping


if __name__ == '__main__':
    main()
