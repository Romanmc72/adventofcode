#!/usr/bin/env python3
"""
Description
-----------
A module for the "nothing is there" coordinate.
"""
from .coordinate import Coordinate
from .symbol import Symbol


class Nothing(Coordinate):
    def __init__(self, x: int, y: int) -> None:
        """A coordinate where it is confirmed nothing is there"""
        super().__init__(x, y, Symbol.NOTHING_THERE)
