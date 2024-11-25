#!/usr/bin/env python3
"""
Description
-----------
Of a complex network of pipes, this class will construct the loops and
sub-loops into a directed graph, or a network of nodes and edges that
represent the pipe and its various connected valves.
"""
from .pipe import Pipe

class Dag:
    def __init__(self):
        pass

    @classmethod
    def from_pipe(self, pipe: Pipe) -> "Dag":
        visited_points = set()
        start_point = pipe.current_valve
