#!/usr/bin/env python3
"""
Description
-----------
A helper module for connecting 2 vertices.
"""
from .coordinate import Coordinate
from .vertex import Vertex


class Line:
    def __init__(self, vertex_a: Vertex, vertex_b: Vertex) -> None:
        self.vertex_a = vertex_a
        self.vertex_b = vertex_b

    def intersects(self, line: "Line") -> bool:
        pass

    def get_intersection(self, line: "Line") -> Coordinate:
        pass

    def __str__(self) -> str:
        return f"{self.vertex_a} -> {self.vertex_b}"

    def __hash__(self) -> int:
        return hash(self.__str__())

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, Line) and self.__hash__() == __value.__hash__()
