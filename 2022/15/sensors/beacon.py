#!/usr/bin/env python3
"""
Description
-----------
Isolated module for the Beacon class.
"""
from .coordinate import Coordinate
from .symbol import Symbol


class Beacon(Coordinate):
    def __init__(self, x: int, y: int) -> None:
        """
        Description
        -----------
        A beacon object that is detected by a sensor.
        """
        super().__init__(x, y, Symbol.BEACON)

    def __hash__(self) -> int:
        return super().__hash__()

    def __eq__(self, __value) -> bool:
        """Determine if this beacon equal to another one."""
        return isinstance(__value, Beacon) and self.__hash__() == __value.__hash__()
