#!/usr/bin/env python3
"""Helper function used in every single module"""
from typing import List


def get_data(input_filename: str = "input.txt", delimiter: str = "\n") -> List[str]:
    """
    Description
    -----------
    Grab the input file and split the contents based on the presence of
    a newline character.

    Params
    ------
    :input_filename: str (default = "input.txt")
    The name of the input file to read.

    :delimiter: str (default = "\\n")
    The delimiter to split the file on. Defaults to a newline.

    Return
    ------
    List[str]
    The list of characters retrieved from the input file. Each element of the
    list represents a line in the file split up by the delimiter.
    """
    with open(input_filename, "r") as f:
        data = f.read()
    return data.split(delimiter)
