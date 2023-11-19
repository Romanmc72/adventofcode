#!/usr/bin/env python3
"""
Description
-----------
Directions (not sure I will actually need these)
"""
from enum import Enum

from .coordinate import Coordinate


class Direction(Enum):
    UP = Coordinate(0, 1)
    DOWN = Coordinate(0, -1)
    LEFT = Coordinate(-1, 0)
    RIGHT = Coordinate(1, 0)
