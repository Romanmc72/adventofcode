#!/usr/bin/env python3
"""
Description
-----------
A helper module for a vertex on the edge of a shape.
"""
from .coordinate import Coordinate


class Vertex(Coordinate):
    def __init__(
        self,
        x: int,
        y: int,
        next_vertex: "Vertex" = None,
        previous_vertex: "Vertex" = None,
    ) -> None:
        super().__init__(x, y)
        self.next_vertex = next_vertex
        self.previous_vertex = previous_vertex

    def set_previous(self, vertex: "Vertex") -> None:
        self.previous_vertex = vertex
        vertex.next_vertex = self

    def set_next(self, vertex: "Vertex") -> None:
        self.next_vertex = vertex
        vertex.previous_vertex = self
