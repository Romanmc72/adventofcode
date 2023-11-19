#!/usr/bin/env python3
"""
Part 1
------
find the first instance of 4 non-repeating characters and the position it occurs

Part 2
------


"""
from collections import deque

from input import get_data


def find_unique_chars(data, num_unique) -> int:
    slider = deque()
    for position, character in enumerate(data):
        if len(set(slider)) == num_unique:
            return position
        slider.append(character)
        if len(slider) > num_unique:
            slider.popleft()


def main():
    data = get_data()
    print(f"Part 1 Position : {find_unique_chars(data, 4)}")
    print(f"Part 2 Position : {find_unique_chars(data, 14)}")


if __name__ == "__main__":
    main()
