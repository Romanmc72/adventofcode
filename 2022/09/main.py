#!/usr/bin/env python3
"""
Part 1
------


Part 2
------


"""
from enum import Enum
from typing import List, Set, Tuple

from input import get_data

class Direction(str, Enum):
    L = "L"
    R = "R"
    U = "U"
    D = "D"
    STAY = "S"


DIRECTION = {
    Direction.L: -1,
    Direction.R: 1,
    Direction.U: 1,
    Direction.D: -1,
    Direction.STAY: 0,
}


class RopePart(Enum):
    HEAD = "HEAD"
    TAIL = "TAIL"


def is_negative(num: int) -> bool:
    """Determines whether a number is negative or not (0 is not negative)"""
    return 0 - num > 0


class LongerRope:
    def __init__(self, length: int = 2):
        if length < 2:
            raise ValueError(f"Rope length must be 2 or more, received {length}")
        self.length = length
        self.tail = [(0, 0) for _ in range(length)]
        self.tail_positions = set([self.tail[-1]])

    def move_head(self, direction: Direction) -> None:
        for tail_part_no, tail_part in enumerate(self.tail):
            if tail_part_no == 0:
                self._move_part(part=tail_part, index=tail_part_no, direction=direction)
            else:
                leader_part_no = tail_part_no - 1
                self._follow_leader(
                    part=tail_part,
                    part_no=tail_part_no,
                    leader=self.tail[leader_part_no],
                )

    def _follow_leader(
        self, part: Tuple[int, int], part_no: int, leader: Tuple[int, int]
    ) -> None:
        x_distance = leader[0] - part[0]
        y_distance = leader[1] - part[1]
        max_distance = max(abs(x_distance), abs(y_distance))
        if max_distance <= 1:
            return None

        moves = []

        if x_distance != 0:
            moves.append(Direction.L if is_negative(x_distance) else Direction.R)

        if y_distance != 0:
            moves.append(Direction.D if is_negative(y_distance) else Direction.U)

        for move in moves:
            self._move_part(self.tail[part_no], part_no, move)

        if part_no == self.length - 1:
            self.tail_positions.add(self.tail[part_no])

    def _move_part(
        self, part: Tuple[int, int], index: int, direction: Direction
    ) -> None:
        if direction in (Direction.L, Direction.R):
            self._move_x(part, index, direction)
        elif direction in (Direction.D, Direction.U):
            self._move_y(part, index, direction)
        else:
            raise ValueError("What?")

    def _move_x(self, part, index, direction) -> None:
        self.tail[index] = (
            part[0] + DIRECTION[direction],
            part[1],
        )

    def _move_y(self, part, index, direction) -> None:
        self.tail[index] = (
            part[0],
            part[1] + DIRECTION[direction],
        )


class Instruction:
    def __init__(self, direction: Direction, magnitude: int):
        self.direction = direction
        self.magnitude = magnitude

    @classmethod
    def from_raw_data(cls, raw_data):
        raw_direction, raw_magnitude = raw_data.split(" ")
        direction = Direction[raw_direction]
        magnitude = int(raw_magnitude)
        return Instruction(direction=direction, magnitude=magnitude)

    def move_rope(self, rope: LongerRope):
        for _ in range(self.magnitude):
            rope.move_head(self.direction)

    def __repr__(self) -> str:
        return f"{self.direction.name} move {self.magnitude}"

    def __str__(self) -> str:
        return self.__repr__()


def main():
    raw_data = get_data()
    rope = LongerRope()
    long_rope = LongerRope(length=10)
    for each_raw_instruction in raw_data:
        instruction = Instruction.from_raw_data(each_raw_instruction)
        instruction.move_rope(rope=rope)
        instruction.move_rope(rope=long_rope)
    print(
        f"Part 1 : The tail of the rope occupied {len(rope.tail_positions)} unique places"
    )
    print(
        f"Part 2 : The tail of the rope occupied {len(long_rope.tail_positions)} unique places"
    )


if __name__ == "__main__":
    main()
