#!/usr/bin/env python3
"""
Description
-----------
Isolated module for the coordinate class.
"""
from enum import Enum

from .symbol import Symbol


class Dimension(str, Enum):
    """The dimensions on the coordinate plane accessible in this program."""

    X = "x"
    Y = "y"


class Coordinate:
    def __init__(self, x: int, y: int, symbol: Symbol = None) -> None:
        """
        Description
        -----------
        A base class used for a particular object that resides within a map
        on an x, y plane.

        Params
        ------
        :x: int
        The x value of the coordinate.

        :y: int
        The y value of the coordinate.

        :symbol: Symbol
        The symbol at the coordinate
        """
        self.x = x
        self.y = y
        self.symbol = symbol

    def distance_between(self, coordinate: "Coordinate") -> int:
        """
        Description
        -----------
        Calculates the [manhattan distance](https://en.wikipedia.org/wiki/Taxicab_geometry
        between the current coordinate and another coordinate"""
        return abs(self.x - coordinate.x) + abs(self.y - coordinate.y)

    def set_symbol(self, symbol: Symbol) -> None:
        """Overrides the currently set symbol."""
        self.symbol = symbol

    def __str__(self):
        """Stringifies the coordinate to its symbol."""
        return str(self.symbol)

    def __repr__(self) -> str:
        return f"{self.__str__()}({Dimension.X}={self.x}, {Dimension.Y}={self.y})"

    def __eq__(self, __value) -> bool:
        """Determine if this coordinate equal to another one."""
        return isinstance(__value, Coordinate) and self.__hash__() == __value.__hash__()

    def __hash__(self) -> int:
        """Generate a hash unique to this coordinate."""
        return hash(self.__repr__())

    def shares_location(self, coordinate: "Coordinate") -> bool:
        return self.x == coordinate.x and self.y == coordinate.y
