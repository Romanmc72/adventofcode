#!/usr/bin/env python3
"""
Part 1
------


Part 2
------


"""
from time import sleep

from input import get_data
from pipeline.path import Path
from pipeline.pipe import Pipe


def main1():
    # pipe = Pipe.from_raw_input(get_data("example.txt"))
    pipe = Pipe.from_raw_input(get_data())
    path = Path(pipe.clone())
    print(pipe)
    return pipe, path

def main2():
    pass


if __name__ == "__main__":
    main1()
    main2()
