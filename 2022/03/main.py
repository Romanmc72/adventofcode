#!/usr/bin/env python3
"""
Part 1
------
Packs are packed incorrectly!

Each might have duplicate items in it

items are letters, case matters

letters have priority a-zA-Z are 1-52 in order

Gotta find all the dupes and the total of the priority

Part 2
------
Now we also need to id which character is in each group of 3 rucks

that letter needs to be identified for the group and the total priority
calculated as well
"""
from string import ascii_letters

PRIORITY_LOOKUP = {
    letter: position + 1 for position, letter in enumerate(ascii_letters)
}

GROUP_SIZE = 3


def main1():
    with open("input.txt", "r") as f:
        data = f.read()

    rucks = data.split("\n")
    priority = 0
    for ruck in rucks:
        ruck_size = len(ruck)
        halfway = ruck_size // 2
        first_half = ruck[:halfway]
        second_half = ruck[halfway:]
        duplicates = set([letter for letter in first_half if letter in second_half])
        for duplicate in duplicates:
            priority += PRIORITY_LOOKUP[duplicate]
    print(f"Part 1 : {priority}")


def main2():
    with open("input.txt", "r") as f:
        data = f.read()

    rucks = data.split("\n")
    priority = 0
    for ruck_group in range(len(rucks) // GROUP_SIZE):
        first_ruck = ruck_group * GROUP_SIZE
        last_ruck = first_ruck + GROUP_SIZE
        ruck_array = rucks[first_ruck:last_ruck]
        for each_letter in ruck_array[0]:
            if each_letter in ruck_array[1] and each_letter in ruck_array[2]:
                priority += PRIORITY_LOOKUP[each_letter]
                break
    print(f"Part 2 : {priority}")


if __name__ == "__main__":
    main1()
    main2()
