#!/usr/bin/env python3
"""
Part 1
------

find the numeric ranges where one completely contains the other!

How many are there?

Part 2
------

find ranges where there is any overlap at all.

How many are there?
"""


def split_pair(pair):
    start, end = pair.split("-")
    return (int(start), int(end))


def get_data():
    with open("input.txt", "r") as f:
        data = f.read()

    lines = data.split("\n")
    for line in lines:
        pairs = line.split(",")
        yield (split_pair(pairs[0]), split_pair(pairs[1]))


def main1():
    """Find the fully overlapped sets"""
    count = 0
    for pair_1, pair_2 in get_data():
        if (pair_1[0] <= pair_2[0] and pair_1[1] >= pair_2[1]) or (
            pair_2[0] <= pair_1[0] and pair_2[1] >= pair_1[1]
        ):
            count += 1
    print(f"Part 1 : {count}")


def main2():
    """
    Count any overlap at all

    Case 1
    .234.....
    ......789

    Case 2
    ......789
    .234.....

    Case 3
    ......789
    .234567..

    Case 4
    .234567..
    ......789

    Case 5
    .234567..
    ..345....

    Case 6
    ..345....
    .234567..
    """
    count = 0
    for pair_1, pair_2 in get_data():
        if (
            (pair_1[0] <= pair_2[0] <= pair_1[1])
            or (pair_1[0] <= pair_2[1] <= pair_1[1])
            or (pair_2[0] <= pair_1[0] <= pair_2[1])
            or (pair_2[0] <= pair_1[1] <= pair_2[1])
        ):
            count += 1
    print(f"Part 2 : {count}")


if __name__ == "__main__":
    main1()
    main2()
