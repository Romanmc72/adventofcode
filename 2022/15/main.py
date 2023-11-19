#!/usr/bin/env python3
"""
Part 1
------
Find out how many confirmed spaces are not a beacon on a given line.

Part 2
------
Find the one unknown spot in a grid where the sensors did not even check
"""
from typing import Tuple

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
        extract_coordinate(beacon_text, Dimension.Y)
    )
    sensor = Sensor(
        extract_coordinate(sensor_text, Dimension.X),
        extract_coordinate(sensor_text, Dimension.Y),
        beacon
    )
    return sensor, beacon


def main1():
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
    print(f"Beginning iteration from {min_x} to {max_x} to count the nothing (that is {order_of_magnitude} orders of magnitude)")
    for x in range(min_x, max_x + 1):
        point = Coordinate(x, y)
        if any([s.distance_between(point) <= s.radius for s in sensors]) and point not in beacons:
            nothings += 1
        iteration = x - min_x
        if iteration % (10**(order_of_magnitude - 2)) == 0:
            print(f"At {x=} {iteration=} with {nothings=}")

    print(f"Counted {nothings} confirmed nothings on line {row}")


def main2():
    sensors = []
    beacons = set()
    shape = Shape(
        Coordinate(0, 0),
        Coordinate(0, 20),
        Coordinate(20, 20),
        Coordinate(20, 0)
    )
    for line in get_data("test.txt"):
        sensor, beacon = parse_points(line)
        sensors.append(sensor)
        beacons.add(beacon)
    empty_shapes = []
    for sensor in sensors:
        sensor.radius += 1
        empty_shapes.append(Shape.from_sensor(sensor))


if __name__ == "__main__":
    main1()
    main2()
