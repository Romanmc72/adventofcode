#!/usr/bin/env python3
"""
Description
-----------
What is more fun than writing code? Writing the same code twice.
"""
from typing import Generator

from .coordinate import Coordinate
from .line import Line
from .sensor import Sensor
from .vertex import Vertex


class Shape:
    def __init__(self, *edges: Coordinate) -> None:
        self.start_vertex = None
        previous_vertex = None
        for edge in edges:
            if not previous_vertex:
                self.start_vertex = Vertex(edge.x, edge.y)
                previous_vertex = self.start_vertex
            else:
                vertex = Vertex(edge.x, edge.y)
                vertex.set_previous(previous_vertex)
                previous_vertex = vertex
        vertex.set_next(self.start_vertex)

    def __iter__(self):
        self.next_vertex = self.start_vertex
        self.first_iteration = True
        return self

    def __next__(self):
        if self.next_vertex == self.start_vertex and not self.first_iteration:
            raise StopIteration
        elif self.next_vertex == self.start_vertex and self.first_iteration:
            self.first_iteration = False
        next_vertex = self.next_vertex
        self.next_vertex = next_vertex.next_vertex
        return next_vertex

    @property
    def lines(self) -> Generator[None, None, Line]:
        for vertex in self:
            yield Line(vertex, vertex.next_vertex)

    @classmethod
    def from_sensor(cls, sensor: Sensor) -> "Shape":
        return cls(*sensor.bounds)

    def subtract(self, shape: "Shape") -> None:
        """
        Description
        -----------
        Takes another shape and subtracts it from the current one. Nothing is
        returned because the current shape is updated by the subtraction.

        Params
        ------
        :shape: Shape
        Input the shape you want to use to subtract from the current shape.
        """
        pass

    def union(self, shape: "Shape") -> None:
        """
        Description
        -----------
        Input the shape you want to add to the current shape. The current shape
        will be updated by this union.

        Params
        ------
        :shape: Shape
        The shape to add to this shape.
        """
        pass

    def intersects(self, shape: "Shape") -> bool:
        for vertex in self:
            pass

    @staticmethod
    def point_within_shape(point, shape) -> bool:
        pass

    @staticmethod
    def line_intersects_shape(line, shape) -> bool:
        pass
