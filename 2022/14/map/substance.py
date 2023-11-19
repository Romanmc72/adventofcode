#!/usr//bin/env python3
"""
Description
-----------
Module to contain the various substances and their symbols.
"""
from enum import Enum


class Substance(str, Enum):
    """
    Description
    -----------
    The enum of substances that can appear on the map.
    """

    SAND = "o"
    ROCK = "#"
    AIR = "."
    SOURCE = "+"
