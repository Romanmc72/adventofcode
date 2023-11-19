#!/usr/bin/env python3
"""
Description
-----------
Isolated module for the sensor class.
"""
from typing import Generator

from .beacon import Beacon
from .coordinate import Coordinate
from .nothing import Nothing
from .symbol import Symbol


class Sensor(Coordinate):
    def __init__(self, x: int, y: int, closest_beacon: Beacon) -> None:
        """
        Description
        -----------
        A sensor object which detects the closest beacon.
        """
        super().__init__(x, y, Symbol.SENSOR)
        self.closest_beacon = closest_beacon

    def list_all_empty_points(self) -> Generator[None, None, Nothing]:
        """
        Description
        -----------
        Yields points within the sensor and it's beacon that do not share a
        location with the beacon. It iterates through all coordinates from
        left to right.

        Return
        ------
        Generator[Coordinate]
        Yields 1 coordinate at a time.
        """
        max_distance = self.distance_between(self.closest_beacon)
        for x in range(-max_distance, max_distance + 1):
            for y in range(-abs(abs(x) - max_distance), abs(abs(x) - max_distance) + 1):
                c = Nothing(x + self.x, y + self.y)
                if not c.shares_location(self.closest_beacon) and not c.shares_location(self):
                    yield c
