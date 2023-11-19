#!/usr/bin/env python3
"""
Description
-----------
Class for a single coordinate value.
"""
from typing import Tuple

from .substance import Substance

COORDINATE_KEY_DELIMITER = ","


class Coordinate:
    def __init__(self, x: int, y: int, substance: Substance) -> None:
        """
        Description
        -----------
        A coordinate on the map of values corresponding to a particular substance.
        """
        self.x = x
        self.y = y
        self.substance = substance
        self.key = Coordinate.coordinate_key(self.x, self.y)
        self.delimiter = COORDINATE_KEY_DELIMITER

    @staticmethod
    def coordinate_key(x: int, y: int) -> str:
        return f"{x}{COORDINATE_KEY_DELIMITER}{y}"

    @staticmethod
    def parse_key(key: str) -> Tuple[int, int]:
        pair = key.split(COORDINATE_KEY_DELIMITER)
        return (int(pair[0]), int(pair[1]))
