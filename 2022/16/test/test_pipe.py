#!/usr/bin/env python3
"""
Description
-----------
Tests the example problem works within the confines of the way the classes
are encoded for solving this problem by replaying the moves made throughout
the example and ensuring that the same results are achieved every time.
"""
from unittest import TestCase

from input import get_data
from pipeline.pipe import Pipe


class TestPipe(TestCase):
    def test_example_problem(self):
        pipe = Pipe.from_raw_input(get_data("example.txt"))
        pipe.move_valve("DD")
        pipe.open_valve()
        pipe.move_valve("AA")
        pipe.move_valve("BB")
        pipe.open_valve()
        pipe.move_valve("AA")
        pipe.move_valve("II")
        pipe.move_valve("JJ")
        pipe.open_valve()
        pipe.move_valve("II")
        pipe.move_valve("AA")
        pipe.move_valve("DD")
        pipe.move_valve("EE")
        pipe.move_valve("FF")
        pipe.move_valve("GG")
        pipe.move_valve("HH")
        pipe.open_valve()
        pipe.move_valve("GG")
        pipe.move_valve("FF")
        pipe.move_valve("EE")
        pipe.open_valve()
        pipe.move_valve("DD")
        pipe.move_valve("CC")
        pipe.open_valve()
        self.assertEqual(pipe.timer, 6)
        self.assertEqual(pipe.released_pressure, 1651)

    def test_every_relationship_is_bi_directional_example(self):
        """
        Asserts that every pipe that leads somewhere also leads back to itself.
        """
        pipe = Pipe.from_raw_input(get_data("example.txt"))
        for valve in pipe.valves:
            for destination_valve in valve.valves:
                self.assertTrue(valve in [v for v in destination_valve.valves])

    def test_every_relationship_is_bi_directional_prompt(self):
        """
        Asserts that every pipe that leads somewhere also leads back to itself.
        """
        pipe = Pipe.from_raw_input(get_data())
        for valve in pipe.valves:
            for destination_valve in valve.valves:
                self.assertTrue(valve in [v for v in destination_valve.valves])
