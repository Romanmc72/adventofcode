#!/usr/bin/env python3
"""
Description
-----------
Isolated module for the Map class.
"""
from typing import List, Tuple

from .beacon import Beacon
from .coordinate import Coordinate, Dimension
from .sensor import Sensor
from .nothing import Nothing
from .unknown import Unknown
from .utils import extract_coordinate


class Map:
    def __init__(self, height: int, width: int, x_offset: int, y_offset: int) -> None:
        """
        Description
        -----------
        The map upon which sensors and beacons reside as coordinates in a grid.

        Params
        ------
        :height: int
        How tall the map is (y coordinates) found via the absolute difference
        between the min y and max y values.

        :width: int
        How wide the map is (x coordinates) found via the absolute difference
        between the min x and max x values.

        :x_offset: int
        The difference between the min x value and zero.

        :y_offset: int
        The difference between the min y value and zero.
        """
        self.height = height
        self.width = width
        self.x_offset = x_offset
        self.y_offset = y_offset
        self.beacons = set()
        self.sensors = list()
        self.coordinates = [
            [Unknown(x, y) for x in range(width)] for y in range(height)
        ]

    def set_coordinate(self, coordinate: Coordinate) -> None:
        """Adds the coordinate to the map."""
        x = coordinate.x + self.x_offset
        y = coordinate.y + self.y_offset
        current_value = self.coordinates[y][x]
        if isinstance(current_value, Unknown):
            self.coordinates[y][x] = coordinate
        else:
            raise ValueError(f"Cannot override {current_value} with {coordinate}")

    def get_coordinate(self, x, y) -> Coordinate:
        """Retrieves a coordinate from the map."""
        return self.coordinates[y + self.y_offset][x + self.x_offset]

    def add_beacon(self, beacon: Beacon) -> None:
        """Adds a beacon to the map and the set of known beacons."""
        if isinstance(self.get_coordinate(beacon.x, beacon.y), Beacon):
            pass
        else:
            self.beacons.add(beacon)
            self.set_coordinate(beacon)

    def add_sensor(self, sensor: Sensor) -> None:
        """Adds a sensor to map and the list of known sensors."""
        self.sensors.append(sensor)
        self.set_coordinate(sensor)

    def add_is_nothing(self, nothing: Nothing) -> None:
        """Sets a point on the map to be a confirmed nothing (skips it if it is a known point)"""
        try:
            if isinstance(self.get_coordinate(nothing.x, nothing.y), Unknown):
                self.set_coordinate(nothing)
        except IndexError:
            pass


    def __str__(self) -> str:
        """Returns the map as a single string to be printable in the terminal"""
        return "\n".join(
            ["".join([str(coord) for coord in row]) for row in self.coordinates]
        )

    # The following methods work excellently for the test data and do as described
    # by the problem to replicate the map shown in the online example. It however
    # fails when your may has sensors and beacons hundreds of thousands of points
    # apart. Keeping these here as they are nice for the test input but they will
    # not work in the actual puzzle input. It is a helpful visualizer for the test
    # but I think I will need to scrap the whole approach for the actual puzzle input.
    @staticmethod
    def parse_raw_data_line(raw_line: str) -> Tuple[Sensor, Beacon]:
        """
        Description
        -----------
        Parses a single line of raw data to get the sensor and beacon from that line.

        Params
        ------
        :raw_line: str
        The raw text to parse for a sensor and beacon.

        Return
        ------
        Tuple[Sensor, Beacon]
        The sensor and the beacon.
        """
        "Sensor at x=2, y=18: closest beacon is at x=-2, y=15"
        sensor_text, beacon_text = raw_line.split(": ")
        beacon = Beacon(
            x=extract_coordinate(beacon_text, Dimension.X),
            y=extract_coordinate(beacon_text, Dimension.Y),
        )
        sensor = Sensor(
            x=extract_coordinate(sensor_text, Dimension.X),
            y=extract_coordinate(sensor_text, Dimension.Y),
            closest_beacon=beacon,
        )
        return sensor, beacon

    @classmethod
    def from_raw_data(cls, raw_data: List[str]) -> "Map":
        """
        Description
        -----------
        Instantiates the map using the raw input data.

        Params
        ------
        :raw_data: List[str]
        The list of strings found for the puzzle input.

        Return
        ------
        Map
        The instantiated map with the input coordinates.
        """
        sensors = []
        beacons = set()
        # Setting these to obscenely large/small values to override them soon
        min_x = 999999999999999999
        max_x = -999999999999999999
        min_y = 999999999999999999
        max_y = -999999999999999999
        for raw_line in raw_data:
            sensor, beacon = Map.parse_raw_data_line(raw_line)
            sensors.append(sensor)
            beacons.add(beacon)
            min_x = min(min_x, sensor.x, beacon.x)
            max_x = max(max_x, sensor.x, beacon.x)
            min_y = min(min_y, sensor.y, beacon.y)
            max_y = max(max_y, sensor.y, beacon.y)
        map = cls(
            height=abs(max_y - min_y) + 1,
            width=abs(max_x - min_x) + 1,
            x_offset=min_x,
            y_offset=min_y,
        )
        for sensor in sensors:
            map.add_sensor(sensor)
        for beacon in beacons:
            map.add_beacon(beacon)
        return map

    def scan_sensor_data(self) -> None:
        """
        Description
        -----------
        Gets the coordinates from all of the sensors that are confirmed to
        be nothing and adds them onto the map.
        """
        nothings = set()
        for sensor in self.sensors:
            for nothing in sensor.list_all_empty_points():
                nothings.add(nothing)
        for nothing in nothings:
            self.add_is_nothing(nothing)

    def count_nothings_in_row(self, row) -> int:
        """Counts up the number of spaces in a row that are confirmed nothing."""
        return len([c for c in self.coordinates[row + self.y_offset] if isinstance(c, Nothing)])
