#!/usr/bin/env python3
"""
Part 1
------
Find out how many confirmed spaces are not a beacon on a given line.

Part 2
------
Find the one unknown spot in a grid where the sensors did not even check.

Going to try and "trace" all the edges of the sensors to find a spot
inside the grid that does not have any sensors detecting it.
"""
import multiprocessing
from copy import deepcopy
from multiprocessing import Pool
from pprint import pprint
from typing import List, Set, Tuple

from input import get_data
from sensors.coordinate import Dimension
from sensors.map import Map
from sensors.utils import extract_coordinate
from shapes.coordinate import Coordinate
from shapes.shape import Shape
from shapes.sensor import Sensor


def parse_points(raw_line: str) -> Tuple[Sensor, Coordinate]:
    sensor_text, beacon_text = raw_line.split(": ")
    beacon = Coordinate(
        extract_coordinate(beacon_text, Dimension.X),
        extract_coordinate(beacon_text, Dimension.Y),
    )
    sensor = Sensor(
        extract_coordinate(sensor_text, Dimension.X),
        extract_coordinate(sensor_text, Dimension.Y),
        beacon,
    )
    return sensor, beacon


def main1():
    """
    Description
    -----------
    Solves part 1 of the problem. The test input and actual input are both
    solved and printed using different solutions. The test solution did not
    scale to the final one because the map was so dang big. Kept it in anyway
    because the visual was nice. The "actual" solution does in fact work with
    the test data as well, it just does not have a nice visual element.
    """
    print("Creating map")
    map = Map.from_raw_data(get_data("test.txt"))
    print("Created map")
    print(map)
    map.scan_sensor_data()
    print("Scanned sensors")
    print(map)
    row = 10
    not_a_beacon = map.count_nothings_in_row(row)
    print(f"There are {not_a_beacon} non-beacons {row=}")

    print("Solving actual puzzle input")
    row = 2000000
    sensors = []
    beacons = set()
    min_x = 99999999999999999
    max_x = -99999999999999999
    for line in get_data():
        sensor, beacon = parse_points(line)
        sensors.append(sensor)
        beacons.add(beacon)
        min_x = min(min_x, beacon.x, sensor.x - sensor.radius)
        max_x = max(max_x, beacon.x, sensor.x + sensor.radius)
    order_of_magnitude = len(str(max_x - min_x))
    y = row
    nothings = 0
    print(
        f"Beginning iteration from {min_x} to {max_x} to count the nothing (that is {order_of_magnitude} orders of magnitude)"
    )
    for x in range(min_x, max_x + 1):
        point = Coordinate(x, y)
        if (
            any([s.distance_between(point) <= s.radius for s in sensors])
            and point not in beacons
        ):
            nothings += 1
        iteration = x - min_x
        if iteration % (10 ** (order_of_magnitude - 2)) == 0:
            print(f"At {x=} {iteration=} with {nothings=}")

    print(f"Counted {nothings} confirmed nothings on line {row}")


def process_one_sensor(
    inputs: Tuple[Sensor, Shape, List[Sensor], int]
) -> Set[Coordinate]:
    """
    Description
    -----------
    This function will process one sensor amidst the list of all sensors and
    the search space of the shape. It will also take in the coordinate
    frequency multiplier. The intention with this method is that you can
    parallelize the searching of all sensors by passing in the required args
    as a tuple and that tuple will be unpacked and processed within the function.

    Params
    ------
    :inputs: Tuple[Sensor, Shape, List[Sensor], int]
    This is the tuple of args that will be unpacked and run byt the function,
    the individual parts are as follows:

    [At index #] :type: description
    [0] :Sensor: sensor to process
    [1] :Shape: the target area to search within
    [2] :List[Sensor]: all fo the other sensors to aide in the search
    [3] :int: the frequency multiplier for the output
    """
    sensor, shape, all_sensors, frequency_multiplier = inputs
    all_sensors.remove(sensor)
    possible_spots = set()
    magnitude = len(str(sensor.radius * 4))
    iteration = 0
    sensor.radius += 1
    for edge in sensor.walk_edge():
        iteration += 1
        if iteration % 10 ** (magnitude - 2) == 0:
            print(f"Iterated through {iteration} points...")
        if shape.contains_point(edge) and not any(
            [s.distance_between(edge) <= s.radius for s in all_sensors]
        ):
            possible_spots.add(edge)
            break
    sensor.radius -= 1
    possible_spots_count = len(possible_spots)
    print(
        f"There {'is' if possible_spots == 1 else 'are'} {possible_spots_count} possible spots"
    )
    for spot in possible_spots:
        print(f"{spot} tuning frequency is: {spot.x * frequency_multiplier + spot.y}")


def main2():
    """
    Description
    -----------
    Solves the second part of the puzzle and uses some parallelism to speed
    up getting the answer. I could add a callback to make the function exit
    when it reaches a solution but I really did not want to work more on this
    one since it is already "done" and "works" despite maybe not being optimal.
    """
    sensors = []
    beacons = set()
    frequency_multiplier = 4000000
    shape = Shape(
        Coordinate(0, 0),
        Coordinate(0, frequency_multiplier),
        Coordinate(frequency_multiplier, frequency_multiplier),
        Coordinate(frequency_multiplier, 0),
    )
    points_to_iterate = 0
    for line in get_data("input.txt"):
        sensor, beacon = parse_points(line)
        sensors.append(sensor)
        beacons.add(beacon)
        points_to_iterate += sensor.radius * 4
    print(f"There are {points_to_iterate=}")
    with Pool((multiprocessing.cpu_count() * 2) - 1) as p:
        p.map(
            process_one_sensor,
            [(sensor, shape, sensors, frequency_multiplier) for sensor in sensors],
        )


if __name__ == "__main__":
    main1()
    main2()
