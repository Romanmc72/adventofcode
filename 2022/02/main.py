#!/usr/bin/env python3
"""
Part 1
------
A = Rock     = 1 Point
B = Paper    = 2 Points
C = Scissors = 3 Points

Loss = 0 Points
Draw = 3 Points
Win  = 6 Points

X = ???
Y = ???
Z = ???

Total Score = ???

Turns out I misread the prompt, it wasn't to find the best case of the possible
scenarios, it was to assume that:

X = Rock
Y = Paper
Z = Scissors

But, I think my way was more fun.

Part 2
------
What X = LOSE, Y = DRAW, Z = WIN the game

What's the score now?
"""
import json
from collections import defaultdict
from itertools import permutations

ROCK = "Rock"
PAPER = "Paper"
SCISSORS = "Scissors"

KEY_LOOKUP = {
    "A": ROCK,
    "B": PAPER,
    "C": SCISSORS,
}

POINT_LOOKUP = {
    ROCK: 1,
    PAPER: 2,
    SCISSORS: 3,
}

UNKNOWN_LOOKUP = ("X", "Y", "Z")

LOSE = 0
DRAW = 3
WIN = 6

GUIDE_TO_TEXT = {
    LOSE: "lose",
    DRAW: "draw",
    WIN: "win",
}

SECRET_LOOKUP = {
    "X": LOSE,
    "Y": DRAW,
    "Z": WIN,
}

STRATEGY_GUIDE = {
    ROCK: {
        LOSE: SCISSORS,
        DRAW: ROCK,
        WIN: PAPER,
    },
    PAPER: {
        LOSE: ROCK,
        DRAW: PAPER,
        WIN: SCISSORS,
    },
    SCISSORS: {
        LOSE: PAPER,
        DRAW: SCISSORS,
        WIN: ROCK,
    },
}

PRINT_BREAK = "===================="


def pprint(j):
    print(json.dumps(j, indent=4, sort_keys=True))


def determine_points(their_move, my_move):
    """Determines the points I receive for a certain outcome"""
    if their_move == my_move:
        outcome = 3
    elif (
        (their_move == ROCK and my_move == PAPER)
        or (their_move == PAPER and my_move == SCISSORS)
        or (their_move == SCISSORS and my_move == ROCK)
    ):
        outcome = 6
    else:
        outcome = 0
    return outcome + POINT_LOOKUP[my_move]


def main1():
    """Rock paper scissors with shifty little elves"""
    with open("input.txt", "r") as f:
        data = f.read()

    lines = data.split("\n")
    pairs = [line.split(" ") for line in lines]
    mapping = defaultdict(lambda: defaultdict(int))
    for opponent, player in pairs:
        mapping[KEY_LOOKUP[opponent]][player] += 1

    possible_scenarios = [
        dict(zip(UNKNOWN_LOOKUP, arrangement))
        for arrangement in permutations([ROCK, PAPER, SCISSORS])
    ]

    for scenario in possible_scenarios:
        total = 0
        for their_move, my_moves in mapping.items():
            for my_move, number_of_times in my_moves.items():
                total += number_of_times * determine_points(
                    their_move,
                    scenario[my_move],
                )
        scenario["total"] = total

    possible_scenarios.sort(key=lambda s: s["total"], reverse=True)

    print(f"Max Score {possible_scenarios[0]['total']}")
    print("Max Score Key:")
    pprint(possible_scenarios[0])
    print(PRINT_BREAK)
    print("All Score Keys:")
    pprint(possible_scenarios)


def main2():
    """Rock paper scissors with shifty little elves"""
    with open("input.txt", "r") as f:
        data = f.read()

    lines = data.split("\n")
    pairs = [line.split(" ") for line in lines]
    mapping = defaultdict(lambda: defaultdict(int))
    for opponent, player in pairs:
        mapping[KEY_LOOKUP[opponent]][SECRET_LOOKUP[player]] += 1

    total = 0
    for their_move, guide in mapping.items():
        for guidance, occurrences in guide.items():
            my_move = STRATEGY_GUIDE[their_move][guidance]
            total += occurrences * determine_points(their_move, my_move)

    print(f"Part 2 : {total}")


if __name__ == "__main__":
    main1()
    main2()
