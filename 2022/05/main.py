#!/usr/bin/env python3
"""
Part 1
------
Figure out what the top crate on every stack will be after all of the moves
are applied to all of the stacks!

Part 2
------
Looks like the stacker moves more than 1 at a time!
"""
import re
from collections import namedtuple
from typing import Dict, List, Tuple

from input import get_data

Instruction = namedtuple("Instruction", "number from_stack to_stack")


class Stack:
    """A stack of crates"""

    def __init__(self, crates: List[str] = [], model: int = 9000):
        self.crates = crates
        if model not in (9000, 9001):
            raise ValueError(f"Incorrect Crate Stacker Model number! {model}")
        self.model = model

    def pick_up_crates(self, number: int) -> List[str]:
        """Picks up the top N crates"""
        if self.model == 9001:
            picked_up = self.crates[-number:]
        else:
            picked_up = self.crates[-number:][-1::-1]
        self.crates = self.crates[:-number]
        return picked_up

    def add_on_crates(self, crates: List[str]) -> None:
        """Add crates onto a stack"""
        self.crates = self.crates + crates



def create_stacks(
    raw_data: List[str], stacker_model: int
) -> Tuple[Dict[int, Stack], List[str]]:
    """
    Parses the raw incoming data and produces the dict of crate stacks to start with.
    Also returns the remainder of the instructions for further parsing
    """
    stack_id_pattern = r"(\s\d+\s+)+"
    for line_no, line in enumerate(raw_data):
        if re.match(stack_id_pattern, line):
            id_line_no = line_no
            stacks = {int(e): Stack(model=stacker_model) for e in line.split("  ")}
            break
    for line in raw_data[(id_line_no - 1) :: -1]:
        crates = line[1::4]
        for stack_no, crate in enumerate(crates, start=1):
            if crate.strip() != "":
                stacks[stack_no].add_on_crates([crate])
            else:
                continue
    return stacks, raw_data[(id_line_no + 2) :]


def create_instructions(raw_data) -> List[Instruction]:
    """
    Parses the text into instructions as a tuple of ints, formatted like:

    (<NUMBER OF CRATES>, <FROM STACK>, <TO STACK>)
    """
    instructions = []
    for line in raw_data:
        first_split = line.split("move ")[1].split(" from ")
        last_split = first_split[1].split(" to ")
        instructions.append(
            Instruction(
                number=int(first_split[0]),
                from_stack=int(last_split[0]),
                to_stack=int(last_split[1]),
            )
        )
    return instructions


def main(stacker_model):
    """
    Main program that will run with different stacker models, the 9000
    moves on crate at a time and the 9001 moves as many as you can want
    """
    raw_data = get_data()
    stacks, remaining_raw_data = create_stacks(
        raw_data=raw_data, stacker_model=stacker_model
    )
    instructions = create_instructions(remaining_raw_data)
    for instruction in instructions:
        stacks[instruction.to_stack].add_on_crates(
            stacks[instruction.from_stack].pick_up_crates(instruction.number)
        )
    stack_keys = list(stacks.keys())
    stack_keys.sort()
    print(f"Model Number {stacker_model} : ", end="")
    for key in stack_keys:
        print(stacks[key].crates[-1], end="")
    print("")


def main2():
    pass


if __name__ == "__main__":
    main(9000)
    main(9001)
