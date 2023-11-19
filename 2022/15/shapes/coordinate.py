#!/usr/bin/env python3
"""
Description
-----------
What is more fun than writing code? Writing the same code twice.
"""


class Coordinate:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y
    
    def __str__(self) -> str:
        x = self.x
        y = self.y
        return f"({x=}, {y=})"

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        return hash(self.__str__())

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, Coordinate) and __value.__hash__() == self.__hash__()

    def distance_between(self, point: "Coordinate") -> int:
        return abs(self.x - point.x) + abs(self.y - point.y)
