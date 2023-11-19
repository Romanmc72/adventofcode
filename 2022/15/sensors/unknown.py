#!/usr/bin/env python3
"""
Description
-----------
A module for the "unknown what is there" coordinate.
"""
from .coordinate import Coordinate
from .symbol import Symbol


class Unknown(Coordinate):
    def __init__(self, x: int, y: int) -> None:
        """A coordinate where we do not know what is there"""
        super().__init__(x, y, Symbol.UNKNOWN)
