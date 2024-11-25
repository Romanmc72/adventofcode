#!/usr/bin/env python3
"""
Description
-----------
Module for a pipeline that exists as a connected set of valves and a timer.
"""
import re
from typing import Callable, Dict, Generator, List

from .exception import TimeIsUpException
from .valve import Valve


class Pipe:
    def __init__(
        self,
        start_valve: Valve = None,
        start_time: int = 30,
        all_valves: Dict[str, Valve] = None,
    ):
        """
        Description
        -----------
        Initializes a pipe object.

        Params
        ------
        :start_valve: Valve (default = None)
        The valve that the person opening the valves begins at.

        :start_time: int (default = 30)
        How much time exists to open the valves in the pipeline.

        :all_valves: Dict[str, Valve] (default = None)
        All of the valves in the pipeline flattened as a dict where the name
        is the key and the value is the Valve.
        """
        self.current_valve = start_valve
        self.timer = start_time
        self.all_valves = all_valves or dict()
        self.released_pressure = 0
        self.out_of_time = start_time <= 0

    @property
    def valves(self) -> Generator[None, None, Valve]:
        for valve in self.all_valves.values():
            yield valve

    def __str__(self) -> str:
        """Represents the pipe as a string, useful for looking at it in the terminal."""
        stringified = [
            f"Time Remaining = {self.timer}",
            f"Released Pressure = {self.released_pressure}\n"
        ]
        for valve in self.valves:
            if valve == self.current_valve:
                stringified.append(f"*{valve}")
            else:
                stringified.append(str(valve))
        stringified.append("\n(* = current valve)")
        return "\n".join(stringified)

    def __repr__(self) -> str:
        return self.__str__()

    @classmethod
    def from_raw_input(cls, raw_input: List[str]) -> "Pipe":
        """
        Description
        -----------
        Given the raw data input, this will generate the Pipe object from that
        raw data.

        Params
        ------
        :raw_input: List[str]
        The list of lines from the input file used to generate the pipe.

        Return
        ------
        Pipe
        The instantiated pipe object.
        """
        pipe = Pipe()
        dependencies = dict()
        for line in raw_input:
            valve = Valve.from_raw_data(line)
            pipe.all_valves[valve.name] = valve
            latter_half = line.split("; ")[-1]
            valve_tunnels_pattern = re.compile(r"([A-Z]{2})")
            downstream_valve_names = re.findall(valve_tunnels_pattern, latter_half)
            dependencies[valve.name] = downstream_valve_names
        for upstream_valve_name, downstream_valves in dependencies.items():
            upstream_valve = pipe.all_valves[upstream_valve_name]
            for downstream_valve in downstream_valves:
                upstream_valve.add_destination(pipe.all_valves[downstream_valve])
        pipe.current_valve = pipe.all_valves["AA"]
        return pipe

    def requires_time(func: Callable, time_cost: int = 1) -> Callable:
        """
        Description
        -----------
        Checks the timer to ensure it is not at or below zero, does the thing
        then decrements the timer by 1. It is to be used as a decorator on other
        class functions that can only run if there is time left to run them.

        Example
        -------

        ```python3
        >>> @requires_time
        >>> def do_a_thing(self):
        ...     # Does something
        ```

        Then by calling do_a_thing() then timer is checked, the function is executed and the
        timer is decremented.

        Params
        ------
        :func: Callable
        The function that this function wraps.

        Return
        ------
        Callable
        The inner function, but wrapped in the time management function.
        """

        def wrapper(self, *args, **kwargs):
            if self.timer - time_cost < 0:
                raise TimeIsUpException(f"Ran out of time trying to {func}")
            self.timer -= time_cost
            self.out_of_time = self.timer <= 0
            return func(self, *args, **kwargs)

        return wrapper

    @requires_time
    def move_valve(self, next_valve: str) -> None:
        """
        Description
        -----------
        Moves from one valve to the next one.

        Params
        ------
        :next_valve: str
        The name of the next valve to move to.
        """
        self.current_valve = self.current_valve.get_destination(next_valve)

    @requires_time
    def open_valve(self) -> None:
        """
        Description
        -----------
        Opens up the current valve and adds the total amount of released
        pressure from that valve to the total released pressure of the pipe.
        """
        self.released_pressure += self.current_valve.open(self.timer)

    def clone(self) -> "Pipe":
        """
        Description
        -----------
        Takes the valves and their state from the current pipe and creates a
        "deep" copy to where you will now have 2 instances of the same pipe
        that can be independently manipulated.
        """
        new_pipe = Pipe()
        for valve in self.valves:
            new_valve = valve.clone()
            new_pipe.all_valves[new_valve.name] = new_valve
        for valve in self.valves:
            for destination_valve in valve.valves:
                new_pipe.all_valves[valve.name].add_destination(
                    new_pipe.all_valves[destination_valve.name]
                )
        new_pipe.timer = self.timer
        new_pipe.current_valve = new_pipe.all_valves[self.current_valve.name]
        return new_pipe

    def possible_moves(self) -> List[Valve]:
        """
        Description
        -----------
        Given the current position, returns the list of possible next moves.

        Return
        ------
        List[Valve]
        The list of valves that can be moved to from the current position.
        """
        return [valve for valve in self.current_valve.valves]

