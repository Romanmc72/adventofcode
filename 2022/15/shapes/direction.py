#!/usr/bin/env python3
"""
Description
-----------
Directions (not sure I will actually need these)
"""
from enum import Enum

from .coordinate import Coordinate


class Direction(Enum):
    """
    Description
    -----------
    Directions as coordinates, useful for multiplying or adding coordinate values.
    """

    UP = Coordinate(0, 1)
    DOWN = Coordinate(0, -1)
    LEFT = Coordinate(-1, 0)
    RIGHT = Coordinate(1, 0)

    @staticmethod
    def next_direction(
        start_direction: "Direction", clockwise: bool = True
    ) -> "Direction":
        """
        Description
        -----------
        Given the direction of start and whether or not you are moving clockwise
        and get the next direction in that rotation.

        Params
        ------
        :start_direction: Direction
        The direction you are starting from.

        :clockwise: bool (default = True)
        Whether or not you are going clockwise.

        Return
        ------
        Direction
        The next direction in the clockwise / counter clockwise rotation.
        """
        if start_direction == Direction.UP:
            if clockwise:
                return Direction.RIGHT
            else:
                return Direction.LEFT
        elif start_direction == Direction.RIGHT:
            if clockwise:
                return Direction.DOWN
            else:
                return Direction.UP
        elif start_direction == Direction.DOWN:
            if clockwise:
                return Direction.LEFT
            else:
                return Direction.RIGHT
        elif start_direction == Direction.LEFT:
            if clockwise:
                return Direction.UP
            else:
                return Direction.DOWN
        else:
            raise ValueError(f"Unknown input direction {start_direction}")
