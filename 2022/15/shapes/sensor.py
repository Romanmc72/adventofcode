#!/usr/bin/env python3
"""
Description
-----------
What is more fun than writing code? Writing the same code twice.
"""
from typing import Tuple

from .coordinate import Coordinate
from .direction import Direction


class Sensor(Coordinate):
    def __init__(self, x: int, y: int, beacon: Coordinate) -> None:
        super().__init__(x, y)
        self.beacon = beacon
        self.radius = self.distance_between(self.beacon)

    def __bounds(self, direction: Direction) -> Coordinate:
        direction = direction.value
        return Coordinate(
            x=self.x + (self.radius * direction.x),
            y=self.y + (self.radius * direction.y)
        )

    @property
    def upper_bound(self) -> Coordinate:
        return self.__bounds(Direction.UP)

    @property
    def lower_bound(self) -> Coordinate:
        return self.__bounds(Direction.DOWN)

    @property
    def left_bound(self) -> Coordinate:
        return self.__bounds(Direction.LEFT)

    @property
    def right_bound(self) -> Coordinate:
        return self.__bounds(Direction.RIGHT)

    @property
    def bounds(self) -> Tuple[Coordinate, Coordinate, Coordinate, Coordinate]:
        return (self.upper_bound, self.right_bound, self.lower_bound, self.left_bound)
