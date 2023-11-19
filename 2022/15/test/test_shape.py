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
    def test_iterate_shape(self):
        shape = Shape.from_sensor(Sensor(0, 0, Coordinate(5, 0)))
        expected_points = set([
            Coordinate(0, 5),
            Coordinate(0, -5),
            Coordinate(5, 0),
            Coordinate(-5, 0),
        ])
        actual_points = set()
        for vertex in shape:
            actual_points.add(vertex)
        self.assertEqual(expected_points, actual_points)

    def test_iterate_lines(self):
        shape = Shape.from_sensor(Sensor(0, 0, Coordinate(5, 0)))
        expected_lines = set([
            Line(Coordinate(0, 5), Coordinate(-5, 0)),
            Line(Coordinate(0, -5), Coordinate(0, 5)),
            Line(Coordinate(5, 0), Coordinate(0, -5)),
            Line(Coordinate(-5, 0), Coordinate(5, 0)),
        ])
        actual_lines = set()
        for line in shape.lines:
            actual_lines.add(line)
        self.assertEqual(expected_lines, actual_lines)

    def test_union_intersecting_shapes(self):
        shared_point = Coordinate(10, 0)
        shape_a = Shape.from_sensor(Sensor(5, 0, shared_point))
        shape_b = Shape.from_sensor(Sensor(15, 0, shared_point))
        shape_a.union(shape_b)

    def test_union_overlapping_shapes(self):
        pass

    def test_union_disjointed_shapes(self):
        pass

    def test_subtract_2_shapes(self):
        pass
