#!/usr/bin/env python3
"""
Description
-----------
What is more fun than writing code? Writing the same code twice.
"""
from typing import Generator, Tuple

from .coordinate import Coordinate
from .direction import Direction


class Sensor(Coordinate):
    def __init__(self, x: int, y: int, beacon: Coordinate) -> None:
        """
        Description
        -----------
        A special kind of Coordinate that has a radius determined by its Manhattan
        distance from another coordinate.

        Params
        ------
        **same x, y from parent coordinate class**

        :beacon: Coordinate
        The "beacon" coordinate that orbits this sensor at the distance of its radius.
        """
        super().__init__(x, y)
        self.beacon = beacon
        self.radius = self.distance_between(self.beacon)

    def __bounds(self, direction: Direction) -> Coordinate:
        """
        Description
        -----------
        Get the sensor's boundary in a given direction

        Params
        ------
        :direction: Direction
        The direction to fetch the boundary of. Given its "shape" is
        diamond-like (because we use manhattan distance), it will return an end
        point on that diamond.

        Return
        ------
        Coordinate
        The point on the edge of the radius at the given direction.
        """
        direction = direction.value
        return Coordinate(
            x=self.x + (self.radius * direction.x),
            y=self.y + (self.radius * direction.y),
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

    def _walk_between_bounds(
        self, start_direction: Direction, clockwise: bool = True
    ) -> Generator[None, None, Coordinate]:
        """
        Description
        -----------
        Traverses between one boundary and its "next" boundary returning every
        point between the two.
        """
        end_direction = Direction.next_direction(start_direction, clockwise)
        translation = start_direction.value.difference(end_direction.value)
        start_bound = self.__bounds(start_direction)
        end_bound = self.__bounds(end_direction)
        current_position = start_bound
        yield current_position
        while current_position != end_bound:
            current_position = Coordinate(
                current_position.x + translation.x, current_position.y + translation.y
            )
            yield current_position

    def walk_edge(self) -> Generator[None, None, Coordinate]:
        """
        Description
        -----------
        Iterate through all of the points on the edge of the radius of the sensor.
        """
        directions = [
            Direction.UP,
            Direction.RIGHT,
            Direction.DOWN,
            Direction.LEFT,
        ]
        for direction in directions:
            for edge_point in self._walk_between_bounds(direction):
                yield edge_point
