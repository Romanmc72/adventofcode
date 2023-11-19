#!/usr/bin/env python3
"""
Part 1
------
Find out how many units of sand can fall before the rest falls to the abyss!

Part 2
------
Turns out there is no abyss, just a floor that goes on forever at max(y) + 2
so find out how much sand comes through until the source is stopped up.

"""
from input import get_data
from map.map import Map


def main1():
    map = Map()
    print("Filling the map")
    map.fill_map(get_data())
    print("The map is filled:")
    print(map)
    iteration = 0
    while not map.full:
        map.drop_sand()
        iteration += 1
        if iteration % 100 == 0:
            print(iteration)
    print(map)
    print(f"Map filled with {map.sand_count} sand")

def main2():
    pass


if __name__ == "__main__":
    main1()
    main2()
