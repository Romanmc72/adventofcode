#!/usr/bin/env python3
"""
Part 1
------
addx = 2 cycles and adds $1 to x during the second cycle
noop = 1 cycles and does nothing

Part 2
------


"""
from typing import List

from input import get_data


class SysClock:
    def __init__(
        self, x: int = 1, clock_offset: int = 20, cycle_time: int = 40
    ) -> None:
        self.x = x
        self.clock = 0
        self.clock_offset = clock_offset
        self.cycle_time = cycle_time
        self.cycle_sum = 0
        self.screen = ""

    @property
    def cycle(self):
        return self.clock + self.clock_offset

    @property
    def is_interval(self):
        return (self.cycle % self.cycle_time) == 0

    @property
    def clock_screen_spot(self):
        return self.clock % self.cycle_time

    def _tick_clock(self) -> None:
        self.clock += 1
        if self.is_interval:
            addon = self.clock * self.x
            self.cycle_sum += addon
        if self.clock_screen_spot == 1:
            self.screen = self.screen + "\n"
        self.screen = self.screen + (
            "#" if self.x <= self.clock_screen_spot < self.x + 3 else "."
        )

    def addx(self, x: int) -> None:
        self._tick_clock()
        self._tick_clock()
        self.x += x

    def noop(self) -> None:
        self._tick_clock()

    @classmethod
    def execute_clock(cls, commands: List[str]):
        sys_clock = cls()
        for command in commands:
            split_command = command.split(" ")
            instruction = split_command[0]
            argument = split_command[-1]
            if instruction == "noop":
                sys_clock.noop()
            elif instruction == "addx":
                x = int(argument)
                sys_clock.addx(x)
        return sys_clock


def main1():
    sys_clock = SysClock.execute_clock(get_data())
    print(f"Signal Strength Sums = {sys_clock.cycle_sum}")
    print(sys_clock.screen)


def main2():
    pass


if __name__ == "__main__":
    main1()
    main2()
