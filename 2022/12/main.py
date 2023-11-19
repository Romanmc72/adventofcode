#!/usr/bin/env python3
"""
Part 1
------
how to travel up to the top! Start from "S" and get to "E"!

Part 2
------
Now you can start from ANY position labeled 'a' instead of just "S" (I just
eyeballed it and moved the "S"). Lucky me all the "b"s were in one column on
one side severely limiting the option set for starting positions.

Although I probably could have just set the `paths' argument when instantiating
the traveler such that they had many starting paths all of which were at a
position labeled `a` instead of just the `S` position.
"""
from collections import defaultdict
from copy import deepcopy
from enum import Enum
from typing import Dict, List, Tuple

from input import get_data


def red(s: str) -> str:
    """
    Description
    -----------
    Input a string and receive that same string but with the ANSI escape code
    for making it appear red in the terminal.

    Params
    ------
    :s: str
    The string to make red

    Return
    ------
    str
    The string, but red
    """
    return f"\u001b[31m{s}\u001b[0m"


def green(s: str) -> str:
    """
    Description
    -----------
    Input a string and receive that same string but with the ANSI escape code
    for making it appear green in the terminal.

    Params
    ------
    :s: str
    The string to make green

    Return
    ------
    str
    The string, but green
    """
    return f"\u001b[32m{s}\u001b[0m"


OFFSET = ord("a")
LOWEST = "S"
HIGHEST = "E"


class Direction(str, Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


INVERSE_DIRECTION = {
    Direction.UP: Direction.DOWN,
    Direction.DOWN: Direction.UP,
    Direction.LEFT: Direction.RIGHT,
    Direction.RIGHT: Direction.LEFT,
}


class Location:
    def __init__(
        self,
        height: int,
        neighbors: Dict[Direction, "Location"] = None,
        highest: bool = False,
        start: bool = False,
    ) -> None:
        """
        Description
        -----------
        Represents an individual location on the map. It will be connected to
        the rest of the locations on the map through the relationship they
        share as "neighbors" and the direction in which that neighbor resides.

        Params
        ------
        :height: int
        How high up this particular location is.

        :neighbors: Dict[Direction, "Location"] (default: None)
        The surrounding locations to this location. A location without
        neighbors is essentially just an island by itself and is
        unreachable and inescapable.

        :highest: bool
        Whether or not this is the highest point.

        :start: bool
        Whether or not this is the starting point.
        """
        self.height = height
        self.neighbors = neighbors or defaultdict(lambda: None)
        self.highest = highest
        self.start = start
        self.moves_to_get_here = -1

    def __str__(self) -> str:
        """
        Description
        -----------
        Represents the Location as a string (just the letter) absent of its neighbors.
        """
        if self.highest:
            return HIGHEST
        if self.start:
            return LOWEST
        return chr(self.height + OFFSET)

    @classmethod
    def from_letter(cls, letter: str) -> "Location":
        """
        Description
        -----------
        Inputting a letter, you will receive a location.

        Params
        ------
        :letter: str
        The letter representing the location's height.

        Return
        ------
        Location
        The location instantiated.
        """
        if letter == LOWEST:
            return cls(height=0, start=True)
        elif letter == HIGHEST:
            return cls(height=ord("z") - OFFSET, highest=True)
        else:
            return cls(height=ord(letter) - OFFSET)

    def connect(
        self, connected_location: "Location", connected_direction: Direction
    ) -> None:
        """
        Description
        -----------
        Connect this location with another and indicate which direction they are
        connected in. The connection will be reciprocated by the connecting
        location if it does not already have an existing neighbor in that direction.

        Params
        ------
        :connected_location: Location
        The location to associate as a neighbor to this current location.

        :connected_direction: Direction
        The direction in which these locations are connected, from the perspective
        of the location calling `.connect()'.

        Example
        -------
        2 Locations share a border, call them 'a' and 'b' and 'a' is to the left
        of 'b'. Conversely 'b' is to the right of 'a'. These 2 calls would be
        identical, and you would only need to call one of them not both.

        tiny map:

        ```
        ab
        ```

        >>> # Instantiate the locations
        >>> location_a = Location.from_letter("a")
        >>> location_b = Location.from_letter("b")
        >>> # This connects them as identified in the above map
        >>> location_a.connect(location_b, Direction.RIGHT)
        >>> # This is the same as the other connect call
        >>> location_b.connect(location_a, Direction.LEFT)

        Return
        ------
        None
        """
        if connected_location is None:
            return None
        else:
            self.neighbors[connected_direction] = connected_location
        if connected_location.neighbors[INVERSE_DIRECTION[connected_direction]] is None:
            connected_location.connect(self, INVERSE_DIRECTION[connected_direction])

    def is_viable(self, neighbor: "Location") -> bool:
        """
        Description
        -----------
        Check whether another location is a "viable" neighbor or in plain speak,
        can I move from my current location to this neighbor. If a location is
        passed in that is not an actual neighbor, this will return False.

        Neighbors can be traveled to only if they are one height higher than the
        current height or lower than that.

        Params
        ------
        :neighbor: Location
        The neighbor that you are checking if you can travel to.

        Return
        ------
        bool
        True if this neighbor can be traveled to
        False if this neighbor cannot be traveled to
        """
        if neighbor not in self.neighbors.values():
            return False
        if neighbor is None:
            return False
        if neighbor.height <= self.height + 1:
            return True
        return False

    def _yield_viable_neighbors(self) -> List[Tuple[Direction, "Location"]]:
        """Internal function, do not call directly."""
        for direction, neighbor in self.neighbors.items():
            if self.is_viable(neighbor=neighbor):
                yield (direction, neighbor)

    def get_viable_neighbors(self) -> List[Tuple[Direction, "Location"]]:
        """
        Description
        -----------
        Get all of the neighbors that from the standpoint of this location
        are considered viable to travel to.

        Return
        ------
        List[Tuple[Direction, "Location"]]
        The list of directions and locations that are viable from this location.
        """
        return [location for location in self._yield_viable_neighbors()]


class Path:
    def __init__(
        self, top: Location, moves: List[Location] = None, has_options: bool = True
    ) -> None:
        """
        Description
        -----------
        A string of locations that have been traveled, or a particular
        "Path" that has been taken.

        Params
        ------
        :top: Location
        The current foremost location.

        :moves: List[Location]
        The list of locations that have been visited on this path in order.

        :has_options: bool
        Whether or not the tip of this path has any options left to travel.
        """
        self.top = top
        self.moves = moves or [top]
        self.has_options = has_options

    @property
    def num_moves(self) -> int:
        """How many moves are in this path (removing the start location)"""
        return len(self.moves) - 1

    @classmethod
    def copy(cls, path: "Path") -> "Path":
        """
        Description
        -----------
        Creates a copy of the path to extend independent of the current one,
        useful for branching.

        Params
        ------
        :path: Path
        The path to create a copy of.

        Return
        ------
        Path
        The copy of the input path.
        """
        return cls(top=path.top, moves=path.moves.copy())

    def move(self, direction: Direction) -> None:
        """
        Description
        -----------
        Take this path from one location to another location in a particular direction.

        Params
        ------
        :direction: Direction
        The direction to move in.
        """
        new_top = self.top.neighbors[direction]
        if not self.top.height + 1 >= new_top.height:
            raise RuntimeError(
                f"current height = {self.top.height} attempted move to {new_top.height}"
            )
        if not new_top:
            self.has_options = False
            return None
        self.top = new_top
        self.moves.append(new_top)
        if self.top.moves_to_get_here == -1:
            self.top.moves_to_get_here = self.num_moves
        else:
            self.top.moves_to_get_here = min(
                self.top.moves_to_get_here, self.num_moves + 1
            )

    def already_been(self, location: Location) -> bool:
        """Whether or not this pat already contains the location."""
        return location in self.moves

    def get_moves(self) -> List[Location]:
        """
        Description
        -----------
        Get all of the viable moves from the current location, considering viability
        both from the location's perspective as well as from the path's perspective.

        Return
        ------
        List[Location]
        The list of locations that are viable moves.
        """
        return [
            neighbor
            for neighbor in self.top.get_viable_neighbors()
            if not self.already_been(neighbor)
        ]


class Map:
    def __init__(self, height: int, width: int, symbols: List[List[str]] = None):
        """
        Description
        -----------
        A purely visual helper for storing and printing out the map of all
        locations in terms of their position and height.

        Params
        ------
        :height: int
        How tall the map is.

        :width: int
        How wide the map is.

        :symbols: List[List[str]] (default = None)
        The array of rows where each row is an array of individual character
        strings that make up the individual coordinates. The first array
        index is the `y` coordinates and the second array index is the `x`
        coordinates. If not specified, the entire map is set to all positions
        as blank strings based on the input height and width.
        """
        self.height = height
        self.width = width
        self.symbols = symbols or [
            [" " for _ in range(self.width)] for _ in range(self.height)
        ]

    def set_symbol(self, x: int, y: int, symbol: str) -> None:
        """
        Description
        -----------
        Override the string for a position on the map using its coordinates and
        the symbol that will take its place.

        Params
        ------
        :x: int
        The `x` coordinate to place the new symbol.

        :y: int
        The `y` coordinate to place the new symbol.

        :symbol: str
        The new symbol to place.
        """
        self.symbols[y][x] = symbol

    def __str__(self) -> None:
        """Prints out the whole map in string form"""
        return "\n".join(
            [
                "".join(
                    [
                        green(symbol) if symbol in (LOWEST, HIGHEST) else symbol
                        for symbol in row
                    ]
                )
                for row in self.symbols
            ]
        )


class Traveler:
    def __init__(
        self,
        start_location: Location,
        paths: List[Path] = None,
    ) -> None:
        """
        Description
        -----------
        Given the start location, this is the traveler who will seek through the map
        using a breadth first search algorithm to find the optimal path to the
        desired end point based on the rules that it can go to any adjacent
        location at most 1 height or it can go to anywhere at or lower than the
        current height.

        Params
        ------
        :start_location: Location
        The location at which the traveler will start its journey to the top.

        :paths: List[Path] (default = None)
        The list of paths that this traveler will be seeded with. Default is
        the will have only 1 path and it will contain their start position only.
        """
        self.start_location = start_location
        self.paths = paths or [Path(top=start_location)]
        self.all_spots = dict()
        for path in self.paths:
            for steps, move in enumerate(path.moves):
                self.all_spots[move] = steps

    def already_been_there(self, location: Location, move_number: int) -> bool:
        """
        Description
        -----------
        Whether or not the traveler has already been to a particular location
        if and only if their having been there was in less moves than is
        currently being compared.

        Params
        ------
        :location: Location
        The location to check if they have already been.

        :move_number: int
        How many moves that the traveler will require to get to this spot
        based on the location/path being compared.

        Return
        ------
        bool
        True if the traveler has already been to this location in the same
        or fewer moves.
        False if the traveler has not been to this location in the same or fewer moves.
        """
        return location in self.all_spots.keys() and move_number >= self.all_spots.get(
            location, 10**10
        )

    def advance_path(
        self, path: Path, location: Location, direction: Direction
    ) -> None:
        """
        Description
        -----------
        Given a path, move the path forward 1 move in a particular direction.

        Params
        ------
        :path: Path
        The path to move forward on.

        :direction: Direction
        The direction to move in on the path.
        """
        path.move(direction=direction)
        self.all_spots[location] = path.num_moves

    def move_to_highest(self) -> None:
        """
        Description
        -----------
        Moves the traveler from the start location to the highest location and
        stores all of the paths that it explored along the way.
        """
        can_still_move = True
        while can_still_move:
            path_copy = self.paths.copy()
            for path in path_copy:
                if not path.has_options:
                    continue
                possible_moves = [
                    move
                    for move in path.get_moves()
                    if not self.already_been_there(move[1], path.num_moves + 1)
                ]
                if len(possible_moves) == 0:
                    path.has_options = False
                elif len(possible_moves) == 1:
                    self.advance_path(path, possible_moves[0][1], possible_moves[0][0])
                else:
                    first_move = True
                    path_clone = Path.copy(path=path)
                    for direction, neighbor in possible_moves:
                        if first_move:
                            self.advance_path(path, neighbor, direction)
                            first_move = False
                        else:
                            re_cloned = Path.copy(path=path_clone)
                            self.advance_path(re_cloned, neighbor, direction)
                            self.paths.append(re_cloned)
            still_more_options = any([path.has_options for path in self.paths])
            reached_highest = any(
                [location.highest for location in self.all_spots.keys()]
            )
            can_still_move = still_more_options and not reached_highest
        print(
            f"Cannot move anymore, more options? {still_more_options}, reached highest? {reached_highest}"
        )

    def show_paths(self):
        """
        Description
        -----------
        Causes the paths that the traveler has gone through to be visually
        presented to the programmer as output in the terminal. The paths will
        be sorted longest to shortest prioritizing first any path that
        actually found the highest point. The paths can be iterated
        through using the keyboard and the instructions will be provided
        to the programmer.
        """
        data = get_data()
        map_height = len(data)
        start_found = False
        end_found = False
        for row_num, row in enumerate(data):
            if LOWEST in row:
                start_y = row_num
                start_x = row.index(LOWEST)
                map_width = len(row)
                start_found = True
            if HIGHEST in row:
                end_y = row_num
                end_x = row.index(HIGHEST)
                end_found = True
            if start_found and end_found:
                break
        default_symbols = [[letter for letter in row] for row in data]
        original_map = path_map = Map(
            map_height, map_width, symbols=deepcopy(default_symbols)
        )
        self.paths.sort(
            key=lambda p: (len(p.moves) * -1) - (10000000 if p.top.highest else 0)
        )
        for path_num, path in enumerate(self.paths):
            path_map = Map(map_height, map_width, symbols=deepcopy(default_symbols))
            path_map.set_symbol(start_x, start_y, LOWEST)
            path_map.set_symbol(end_x, end_y, HIGHEST)
            cursor_x = start_x
            cursor_y = start_y
            for move_num, move in enumerate(path.moves):
                try:
                    next_move = path.moves[move_num + 1]
                    for direction, neighbor in move.neighbors.items():
                        if next_move == neighbor:
                            if direction == Direction.UP:
                                # "up" is minus because the grid starts in the top left and goes
                                # "down" on the screen as the coordinates increase and goes
                                # "up" on the screen as coordinates decrease.
                                cursor_y -= 1
                            elif direction == Direction.DOWN:
                                cursor_y += 1
                            elif direction == Direction.RIGHT:
                                cursor_x += 1
                            elif direction == Direction.LEFT:
                                cursor_x -= 1
                            symbol = red(neighbor)
                            path_map.set_symbol(cursor_x, cursor_y, symbol)
                            break
                except IndexError:
                    next_move = None
            if path.top.highest:
                also = "and it reached the end! \N{shooting star}"
            else:
                also = ""
            print(f"This is path {path_num + 1} out of {len(self.paths)} paths")
            print(f"There are {path.num_moves} moves on this path {also}")
            print(path_map)
            inp = None
            while inp != "":
                inp = input(
                    f"Press Enter to continue, 'o' to show original"
                    + " or 'a' to print this path again or 'q' to quit..."
                )
                if inp == "o":
                    print(original_map)
                if inp == "a":
                    print(path_map)
                if inp == "q":
                    exit(0)


def create_map(raw_data: List[str]) -> Traveler:
    """
    Description
    -----------
    Given the input data, create all of the locations and place the traveler
    on the map at the start location.
    """
    start = None
    current_row = []
    above_row = []
    up = None
    for row_num, row in enumerate(raw_data):
        left = None
        above_row = current_row
        current_row = []
        for character_num, character in enumerate(row):
            location = Location.from_letter(character)
            location.connect(left, Direction.LEFT)
            if row_num == 0:
                up = None
            else:
                up = above_row[character_num]
            location.connect(up, Direction.UP)
            if location.start:
                start = location
            current_row.append(location)
            left = location
    return Traveler(start_location=start)


def main():
    traveler = create_map(get_data())
    traveler.move_to_highest()
    for path in traveler.paths:
        if path.top.highest:
            print(f"Reached highest in {path.top.moves_to_get_here}")
    traveler.show_paths()


if __name__ == "__main__":
    main()
