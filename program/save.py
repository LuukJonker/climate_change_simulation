import functools
import time


def Coordinates(coordinates, ghg, albedo):
    return True


def timer(func):
    """Print the runtime of the decorated function"""
    @functools.wraps(func)
    def wrapper_timer(*args, **kwargs):
        start_time = time.perf_counter()    # 1
        value = func(*args, **kwargs)
        end_time = time.perf_counter()      # 2
        run_time = end_time - start_time    # 3
        print(f"Finished {func.__name__!r} in {run_time:.4f} secs")
        return value
    return wrapper_timer


@timer
def create_list_coordinate(interval):
    x_interval, y_interval = int(360 / interval), int(180 / interval)
    coordinates_list = []
    for x in range(x_interval):
        new_list = []
        for y in range(y_interval):
            new_list.append(Coordinates((x * x_interval, y * y_interval), 0, 0))
        coordinates_list.append(new_list)



@timer
def create_list_coordinates(interval):
    x_interval, y_interval = int(360 / interval), int(180 / interval)
    coordinates_list = [[None] * y_interval] * x_interval
    for x, x_value in enumerate(coordinates_list):
        for y, _ in enumerate(x_value):
            coordinates_list[x][y] = Coordinates((x * x_interval, y * y_interval), 0, 0)
    return coordinates_list
