#!/usr/bin/env python3
"""
Description
-----------
Unit tests for the shape class. Going to try some test driven development
where I write what I expect to happen here then edit the code and write the
test hoping it passes one day soon.
"""
from unittest import TestCase

from shapes.coordinate import Coordinate
from shapes.line import Line
from shapes.shape import Shape
from shapes.sensor import Sensor


class TestShape(TestCase):
    def test_point_in_shape(self):
        point = Coordinate(1, 1)
        shape = Shape(
            Coordinate(0, 0), Coordinate(2, 0), Coordinate(2, 2), Coordinate(0, 2)
        )
        self.assertTrue(shape.contains_point(point))

    def test_point_in_shape_on_edge(self):
        point = Coordinate(2, 2)
        shape = Shape(
            Coordinate(0, 0), Coordinate(2, 0), Coordinate(2, 2), Coordinate(0, 2)
        )
        self.assertTrue(shape.contains_point(point))

    def test_point_not_in_shape(self):
        point = Coordinate(20, 20)
        shape = Shape(
            Coordinate(0, 0), Coordinate(2, 0), Coordinate(2, 2), Coordinate(0, 2)
        )
        self.assertFalse(shape.contains_point(point))
