#!/usr/bin/env python3
"""
Description
-----------
Generic utility for parsing the raw data, or methods that don't belong in a class.
"""
import re

from .coordinate import Dimension


def extract_coordinate(text: str, dimension: Dimension) -> int:
    """
    Description
    -----------
    Using the input text, pull out from it the specific X or Y coordinate
    numeric value.

    Params
    ------
    :text: str
    The text from which to extract a coordinate.

    :dimension: Dimension
    The X or Y dimension that is being extracted from the text.

    Return
    ------
    int
    The numeric value at that position.
    """
    # The pattern states that it is searching for a number possibly with a
    # negative symbol in front of it, and with one or more digits after that
    # negative symbol. It must also be preceded by the dimension ("x" or "y")
    # and an "="" sign but we do not wish to extract the dimension or =.
    pattern = re.compile(f"(?<={dimension}=)(-?\d+)")
    coordinate = int(re.findall(pattern, text)[0])
    return coordinate
