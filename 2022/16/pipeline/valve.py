#!/usr/bin/env python3
"""
Description
-----------
This is a helper module for a valve object. Valves lead to other valves and
they have a flow rate.
"""
import re
from typing import Dict, Set, Tuple

from .exception import AlreadyOpen


class Valve:
    def __init__(
        self,
        name: str,
        flow_rate: int = 0,
        valves: Dict[str, "Valve"] = None,
        is_open: bool = False,
    ) -> None:
        """
        Description
        -----------
        Instantiates a valve object.

        Params
        ------
        :name: str
        The string name of this valve.

        :flow_rate: int (default = 0)
        The amount of flow that this valve yields per minute when it is opened.

        :valves: Dict[str, Valve] (default = None)
        The valves downstream of this one stored as key-value pairs
        where the key is the valve name.

        :is_open: bool (default = False)
        Whether or not this valve is open.
        """
        self.name = name
        self.flow_rate = flow_rate
        self.is_open = is_open
        self._valves = valves or dict()

    @property
    def valves(self):
        for valve in self._valves.values():
            yield valve

    def __symbolized(self) -> str:
        """Turns the valve into an symbol of its name and whether or not it is open"""
        return f">{self.name}<" if self.is_open else f"<{self.name}:{self.flow_rate}>"

    def __str__(self) -> str:
        """The stringified representation of a valve."""
        return f"{self.__symbolized()} -> [{', '.join([v.__symbolized() for v in self.valves])}]"

    def __repr__(self) -> str:
        """The valve as shown in the terminal."""
        return self.__str__()

    def __hash__(self) -> int:
        """The hash of this valve"""
        return hash(self.name)

    def __eq__(self, __value) -> bool:
        """Whether or not this valve is the same as another thing"""
        return (
            isinstance(__value, Valve)
            and self.flow_rate == __value.flow_rate
            and self.is_open == __value.is_open
            and self.__hash__() == __value.__hash__()
        )

    @classmethod
    def from_raw_data(cls, raw_data: str) -> "Valve":
        """
        Description
        -----------
        Parses the raw string input into a valve.

        Params
        ------
        :raw_data: str
        The line of raw data from the input that contains the info for a
        particular valve.
        """
        valve_name_pattern = re.compile(r"^Valve ([A-Z]+) ")
        flow_rate_pattern = re.compile(r"flow rate=(\d+);")
        valve_name = re.findall(valve_name_pattern, raw_data)[0]
        flow_rate = int(re.findall(flow_rate_pattern, raw_data)[0])
        return cls(name=valve_name, flow_rate=flow_rate)

    def get_destination(self, valve_name: str) -> "Valve":
        """
        Description
        -----------
        Retrieve a valve from the downstream destination valves using the name
        of that valve. If a valve is requested but does not exist in the set
        of destination valves then an error will be raised.

        Params
        ------
        :valve_name: str
        The name of the destination valve to retrieve.

        Return
        ------
        Valve
        The requested valve.

        Raises
        ------
        KeyError
        If the requested valve does not exist in the destinations.
        """
        try:
            return self._valves[valve_name]
        except KeyError:
            raise KeyError(
                f"Valve {self} does not contain {valve_name=} in"
                + " its destination valves."
            )

    def add_destination(self, valve: "Valve") -> None:
        """
        Description
        -----------
        Adds a destination valve to the valve.

        Params
        ------
        :valve: Valve
        The valve downstream of this one.
        """
        self._valves[valve.name] = valve

    def open(self, time: int) -> int:
        """
        Description
        -----------
        Opens a valve and returns all of the released pressure from that valve
        given the amount of time input and the flow rate of the valve.

        Params
        ------
        :time: int
        The time remaining.

        Return
        ------
        int
        time * self.flow_rate
        The amount of flow released by this valve for the rest of the pipeline.
        """
        if self.is_open:
            raise AlreadyOpen(f"Attempted to open {self} but it is {self.is_open=}")
        self.is_open = True
        return self.flow_rate * time

    def clone(self) -> "Valve":
        """
        Description
        -----------
        Clones this valve without cloning any of its destination valves.
        Those will need to be reattached using their clones.
        """
        return Valve(name=self.name, flow_rate=self.flow_rate, is_open=self.is_open)

    def has_connected_flow(self, exclude: Set["Valve"] = None) -> bool:
        """
        Description
        -----------
        Whether or not this valve has available flow rate or any downstream
        valves have available flow.
        """
        if not exclude:
            exclude = set()
        exclude.add(self)
        return (
            (self.flow_rate > 0 and not self.is_open)
            or any([
                valve.has_connected_flow(exclude)
                for valve in self.valves
                if valve not in exclude
            ])
        )

    def get_total_connected_flow(self, levels: int, timer:int, exclude: Set["Valve"] = None, pathway: Tuple[str] = None) -> Tuple[Tuple[str],int]:
        """
        Description
        -----------
        Total up all of the flow that is connected downstream of this valve.

        Params
        ------
        :levels: int
        How many levels deep to search recursively.

        :timer: int
        What the timer is currently at.

        :exclude: Set[Valve] (default = None)
        The set of valves that have already been visited on this search.

        Return
        ------
        Tuple[Tuple[str],int]
        (path_tuple, total_flow)
        The tuple of 2 values, the path as a set of strings connecting the
        various valves by name and then the total amount of flow releasable
        by the valves on that path.
        """
        if not pathway:
            pathway = tuple()
        if levels <= 0:
            return pathway, 0
        if not exclude:
            exclude = set()
        exclude.add(self)
        if levels == 1:
            return pathway + tuple([self.name]), self.flow_rate
        open_multiplier = 0 if self.is_open else 1
        pathway += tuple([self.name])
        total_flow = self.flow_rate * timer * open_multiplier
        for valve in self.valves:
            if valve not in exclude and not valve.is_open:
                updated_path, updated_flow = valve.get_total_connected_flow(
                    levels=levels - 1,
                    timer=timer - 1,
                    exclude=exclude,
                    pathway=pathway
                )
                pathway += updated_path
                total_flow += updated_flow
        return pathway, total_flow
