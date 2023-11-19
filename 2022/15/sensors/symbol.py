#!/usr/bin/env python3
"""
Description
-----------
Module for the shared string symbols used in the program.
"""
from enum import Enum


class Symbol(str, Enum):
    """Shared symbols referenced by parts of the program."""

    def __str__(self) -> str:
        return str(self.value)

    BEACON = "B"
    SENSOR = "S"
    NOTHING_THERE = "#"
    UNKNOWN = "."
