#!/usr/bin/env python3
"""
Description
-----------
Module for the pathway between valves in a pipe.
"""
from .pipe import Pipe
from .valve import Valve


class Path:
    def __init__(self, pipe: Pipe) -> None:
        """
        Description
        -----------
        Initializes the Path object which stores a specific traversal of a
        pipe from one valve to the next with the actions taken along the way.
        """
        self.pipe = pipe

    def search_for_highest_points(self) -> Valve:
        """
        Description
        -----------
        Given the current set of possible moves, pick the one that has the highest
        """
        move_map = dict()
        for possible_move in self.pipe.possible_moves():
            if possible_move.has_connected_flow():
                move_map[possible_move] = possible_move.get_total_connected_flow(
                    levels=self.pipe.timer - 1,
                    timer=self.pipe.timer,
                )
        move_list = list(move_map.items())
        move_list.sort(key=lambda k_v_pair: -k_v_pair[1][1])
        return move_list
        # best_move = move_list[0][0]
        # return best_move
