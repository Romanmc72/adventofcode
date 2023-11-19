#!/usr/bin/env python3
"""
Tests that the sensor works as intended
"""
from unittest import TestCase

from sensors.beacon import Beacon
from sensors.sensor import Sensor
from sensors.nothing import Nothing

class TestSensor(TestCase):
    def test_list_all_empty_points_origin(self):
        b = Beacon(-3, 1)
        s = Sensor(0, 0, b)
        expected_points = set([
            Nothing(-4, 0),
            Nothing(-3, -1),
            Nothing(-3, 0),
            # Skips this point, it is the beacon
            # Nothing(-3, 1),
            Nothing(-2, -2),
            Nothing(-2, -1),
            Nothing(-2, 0),
            Nothing(-2, 1),
            Nothing(-2, 2),
            Nothing(-1, -3),
            Nothing(-1, -2),
            Nothing(-1, -1),
            Nothing(-1, 0),
            Nothing(-1, 1),
            Nothing(-1, 2),
            Nothing(-1, 3),
            Nothing(0, -4),
            Nothing(0, -3),
            Nothing(0, -2),
            Nothing(0, -1),
            # skips this point, it is itself
            # Nothing(0, 0),
            Nothing(0, 1),
            Nothing(0, 2),
            Nothing(0, 3),
            Nothing(0, 4),
            Nothing(1, -3),
            Nothing(1, -2),
            Nothing(1, -1),
            Nothing(1, -0),
            Nothing(1, 1),
            Nothing(1, 2),
            Nothing(1, 3),
            Nothing(2, -2),
            Nothing(2, -1),
            Nothing(2, 0),
            Nothing(2, 1),
            Nothing(2, 2),
            Nothing(3, -1),
            Nothing(3, 0),
            Nothing(3, 1),
            Nothing(4, 0),
        ])
        actual_points = set()
        for point in s.list_all_empty_points():
            actual_points.add(point)
        self.assertEqual(expected_points, actual_points)

    def test_list_all_empty_points_offset(self):
        b = Beacon(-3, 1)
        s = Sensor(-3, 0, b)
        expected_points = set([
            Nothing(-3, -1),
            Nothing(-2, 0),
            Nothing(-4, 0),
        ])
        actual_points = set()
        for point in s.list_all_empty_points():
            actual_points.add(point)
        self.assertEqual(expected_points, actual_points)
