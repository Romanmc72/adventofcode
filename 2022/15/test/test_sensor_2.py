#!/usr/bin/env python3
"""
Tests that the sensor works as intended
"""
from unittest import TestCase

from shapes.coordinate import Coordinate
from shapes.sensor import Sensor


class TestSensor(TestCase):
    def test_walk_edges(self):
        expected_edges = set(
            [
                Coordinate(0, 3),
                Coordinate(-1, 2),
                Coordinate(-2, 1),
                Coordinate(-3, 0),
                Coordinate(-2, -1),
                Coordinate(-1, -2),
                Coordinate(0, -3),
                Coordinate(1, -2),
                Coordinate(2, -1),
                Coordinate(3, 0),
                Coordinate(2, 1),
                Coordinate(1, 2),
            ]
        )
        sensor = Sensor(0, 0, Coordinate(0, 3))
        actual_edges = set()
        for edge in sensor.walk_edge():
            actual_edges.add(edge)
        self.assertEqual(expected_edges, actual_edges)
