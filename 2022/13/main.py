#!/usr/bin/env python3
"""
Part 1
------
Find the pairs that are correctly sorted and sum their index values.

Part 2
------
Sort all the pairs and add in a bonus 2 elements of [[2]] and [[6]] then return
the product of the index values for the bonus pair locations.
"""
import json
import logging
from json.decoder import JSONDecodeError
from collections import namedtuple
from pprint import pprint
from typing import List

from input import get_data

logging.basicConfig()
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.WARN)

BONUS_1 = [[2]]
BONUS_2 = [[6]]


Pair = namedtuple("Pair", ["left", "right"])


def parse_pairs(input_data: List[str]) -> List[Pair]:
    """
    Description
    -----------
    Parses the input data into pairs of values with a left and a right.

    Params
    ------
    :input_data: List[str]
    The list of input strings to be parsed.

    Return
    ------
    List[Pair]
    The list of pairs all parsed out.
    """
    left = None
    pair = None
    next_is_left = True
    pairs = []
    for line in input_data:
        try:
            parsed_line = json.loads(line.strip())
        except JSONDecodeError:
            pairs.append(pair)
            continue
        if next_is_left:
            left = parsed_line
            next_is_left = False
        else:
            pair = Pair(left, parsed_line)
            next_is_left = True
    pairs.append(pair)
    return pairs


def compare_pair(pair: Pair) -> bool:
    """
    Description
    -----------
    Returns True if the pairs are ordered correctly and false if not.
    """
    LOGGER.debug(f"Comparing {pair}")
    compared_value = None
    position = 0
    left_value = None
    for position, left_value in enumerate(pair.left):
        try:
            right_value = pair.right[position]
            if isinstance(left_value, int) and isinstance(right_value, int):
                if left_value < right_value:
                    LOGGER.debug(f"{left_value} < {right_value} sorted = True")
                    return True
                elif left_value > right_value:
                    LOGGER.debug(f"{left_value} > {right_value} sorted = False")
                    return False
                else:
                    LOGGER.debug(f"{left_value} == {right_value} skipping")
                    continue
            elif isinstance(left_value, list) and isinstance(right_value, list):
                LOGGER.debug("Both are lists, diving in...")
                compared_value = compare_pair(Pair(left=left_value, right=right_value))
            elif isinstance(left_value, int) and isinstance(right_value, list):
                LOGGER.debug(
                    f"Left is an int {left_value} and right is a list {right_value},"
                    + " wrapping left in a list and comparing..."
                )
                compared_value = compare_pair(
                    Pair(left=[left_value], right=right_value)
                )
            elif isinstance(left_value, list) and isinstance(right_value, int):
                LOGGER.debug(
                    f"Left is a list {left_value} and right is an int {right_value},"
                    + " wrapping right in a list and comparing..."
                )
                compared_value = compare_pair(
                    Pair(left=left_value, right=[right_value])
                )
            if compared_value is None:
                LOGGER.debug("That sub-comparison did not solve it. Moving on.")
                continue
            else:
                LOGGER.debug("That sub-comparison did solve it!")
                return compared_value
        except IndexError:
            # The index error here signals that the left side had a value present but
            # the right side did not therefore the pair is not correctly ordered.
            LOGGER.debug(
                "Looks like the right side ran out of elements, returning False"
                + f" {pair} at position {position}"
            )
            return False
    try:
        # If the left side is out of elements and the right side still has one
        # or more left, this pair is correctly ordered
        pair.right[position + 1]
        LOGGER.debug(
            "The left side is all out of elements and the right has 1 more,"
            + f" this is correctly sorted. {pair} at {position}"
        )
        return True
    except IndexError:
        try:
            if position == 0 and left_value is None:
                pair.right[position]
                LOGGER.debug(
                    "The left side did not have any elements but the right did,"
                    + f" returning True. {pair} at {position}"
                )
                return True
            else:
                LOGGER.debug(f"Moving on, nothing gained from this comparison. {pair}")
                return None
        except IndexError:
            return None


def main1():
    """
    Description
    -----------
    Gives the correct answer for part 1
    """
    index_sum = 0
    pairs = parse_pairs(get_data())
    compared = [compare_pair(pair) for pair in pairs]
    for index, correctly_ordered in enumerate(compared):
        if correctly_ordered:
            index_sum += index + 1
    print(f"Solution is : {index_sum}")


def parse_all_values(input_data: List[str]) -> list:
    """
    Description
    -----------
    Simply given the input, parse out all the values then add in the "bonus pairs".

    Params
    ------
    :input_data: List[str]
    The raw data to parse.

    Return
    ------
    list
    The list of lists of lists of integers or whatever.
    """
    output_data = []
    for line in input_data:
        if line == "":
            continue
        else:
            output_data.append(json.loads(line))
    output_data.append([[2]])
    output_data.append([[6]])
    return output_data


def sort_list(parsed_list: list, sorted_list: list = None, start_at: int = 0) -> list:
    """
    Description
    -----------
    Sorts the input list into the correct order and returns it.


    The sorting algorithm works as follows:

    say you have the following numbers

    [2, 5, 6, 3, 1, 7, 9, 8, 0, 4]

    and you want them sorted in ascending order.

    This algorithm will look at the first element and the one immediately
    following it. If they are in ascending order, it will look at the next
    element, adding the elements it has already seen to a running list.

    Like so

    [2, 5, 6, 3, 1, 7, 9, 8, 0, 4]
     ^  ^
     2<=5 True
    list = [2, 5]

    [2, 5, 6, 3, 1, 7, 9, 8, 0, 4]
        ^  ^
        5<=6 True
    list = [2, 5, 6]

    [2, 5, 6, 3, 1, 7, 9, 8, 0, 4]
           ^  ^
           6<=3 False

    In the event we come into contact with an element that is out of order, we
    will take that element and compare it to our running list traversing it from
    start to finish with the opposite comparison.
    Like so

    list = [2, 5, 6]
    unsorted_element = 3

    [2, 5, 6]
     ^
     2 >= 3 False

    check next
    [2, 5, 6]
        ^
        5 >= 3 True!

    Therefore the unsorted element goes between 2 and 5, and we can continue
    on our journey using the head of the running list against the remainder
    of our unsorted data. In the event we come across an item that finds no
    elements in our running list that are less than it is, we can take that
    item and place it at the start of the running list. It might save us
    some time to do that initial check first to avoid reverse traversing
    the whole list every time we find a new smallest item, but it could also
    add the burden of another check that is done unnecessarily.

    Params
    ------
    :parsed_list: list
    The list of freshly parsed data.

    :sorted_list: list
    The list of sorted data so far.

    :start_at:
    Where to start the sorting search from.

    Return
    ------
    The parsed data sorted out.
    """
    sorted_list = []
    first_iteration = True
    for unsorted_element in parsed_list:
        if first_iteration:
            sorted_list.append(unsorted_element)
            first_iteration = False
            continue
        if compare_pair(Pair(left=sorted_list[-1], right=unsorted_element)):
            sorted_list.append(unsorted_element)
        else:
            for index, sorted_element in enumerate(sorted_list):
                if compare_pair(Pair(left=unsorted_element, right=sorted_element)):
                    sorted_list.insert(index, unsorted_element)
                    break
    return sorted_list


def is_correctly_sorted(sorted_list: list) -> bool:
    """
    Description
    -----------
    Spot checks the entire array to see if each element is correctly sorted as
    compared to the one that comes after it.

    Params
    ------
    :sorted_list: list
    The list of items that should be sorted.

    Return
    ------
    bool
    True if it is correctly sorted.
    False if it is not correctly sorted.
    """
    is_sorted = True
    for index, element in enumerate(sorted_list):
        try:
            is_sorted = is_sorted and compare_pair(
                Pair(element, sorted_list[index + 1])
            )
            if not is_sorted:
                return is_sorted
        except IndexError:
            continue
    return is_sorted


def main2():
    """
    Description
    -----------
    Gives the correct answer for part 2.
    """
    parsed_list = parse_all_values(get_data())
    print(f"Part 2 has: {len(parsed_list)} elements")
    sorted_list = sort_list(parsed_list)
    print(f"Is that list sorted? {is_correctly_sorted(sorted_list)}")
    # Adding 1 because this problem uses a 1-based index
    bonus_1_index = sorted_list.index(BONUS_1) + 1
    bonus_2_index = sorted_list.index(BONUS_2) + 1
    print(f"The decoder key is {bonus_1_index * bonus_2_index}")


if __name__ == "__main__":
    main1()
    main2()
