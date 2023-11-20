#!/usr/bin/env python3
"""
Description
-----------
What is more fun than writing code? Writing the same code twice.
"""


class Coordinate:
    def __init__(self, x: int, y: int) -> None:
        """
        Description
        -----------
        An X, Y point in 2 dimensional space.

        Params
        ------
        :x: int
        The x coordinate.

        :y: int
        The y coordinate.
        """
        self.x = x
        self.y = y

    def __str__(self) -> str:
        """How a coordinate is represented in a string."""
        x = self.x
        y = self.y
        return f"({x=}, {y=})"

    def __repr__(self) -> str:
        """How a coordinate object is represented in the terminal."""
        return self.__str__()

    def __hash__(self) -> int:
        """Return a hash uniquely identifying this coordinate."""
        return hash(self.__str__())

    def __eq__(self, __value: object) -> bool:
        """Determine if 2 coordinates are equal."""
        return isinstance(__value, Coordinate) and __value.__hash__() == self.__hash__()

    def distance_between(self, point: "Coordinate") -> int:
        """Get the distance between 2 points in absolute terms."""
        return abs(self.x - point.x) + abs(self.y - point.y)

    def difference(self, coordinate: "Coordinate") -> "Coordinate":
        """Get the difference between 2 points as a coordinate."""
        return Coordinate(coordinate.x - self.x, coordinate.y - self.y)
