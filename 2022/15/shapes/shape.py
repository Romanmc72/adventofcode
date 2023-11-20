#!/usr/bin/env python3
"""
Description
-----------
What is more fun than writing code? Writing the same code twice.
"""
from .coordinate import Coordinate
from .vertex import Vertex


class Shape:
    def __init__(self, *edges: Coordinate) -> None:
        """
        Description
        -----------
        I made this class with the intention of doing linear algebra to union
        and subtract shapes from one another by navigating the vertices and
        doing math but that was going to be super involved and take less time
        than using a more brute force solution. The __init__ method is agnostic
        to the polygon you put in and the number of vertices but this really
        only works in the context of solving this problem if you use the class
        to construct a rectangle and use the `contains_point()` method.

        Params
        ------
        :*edges: Coordinate
        A list of coordinates that make up the vertices of this shape. Only
        Rectangular shapes will solve the problem, but any shape will be
        accepted byu the init method.
        """
        self.min_x = 999999999999999
        self.min_y = 999999999999999
        self.max_x = -999999999999999
        self.max_y = -999999999999999
        self.start_vertex = None
        previous_vertex = None
        for edge in edges:
            self.min_x = min(self.min_x, edge.x)
            self.min_y = min(self.min_y, edge.y)
            self.max_x = max(self.max_x, edge.x)
            self.max_y = max(self.max_y, edge.y)
            if not previous_vertex:
                self.start_vertex = Vertex(edge.x, edge.y)
                previous_vertex = self.start_vertex
            else:
                vertex = Vertex(edge.x, edge.y)
                vertex.set_previous(previous_vertex)
                previous_vertex = vertex
        vertex.set_next(self.start_vertex)

    def contains_point(self, point) -> bool:
        """
        Description
        -----------
        This tells you whether or not an input point is within the larger shape.
        This only works if your shape is rectangular. The shapes boundaries are
        inclusive so if it lies on the edge it will return true.

        Params
        ------
        :point: Coordinate
        The point to tell if it is inside or not.

        Return
        ------
        bool
        True if the point is in the shape.
        False if the point is not in the shape.
        """
        return (
            self.min_x <= point.x <= self.max_x and self.min_y <= point.y <= self.max_y
        )
