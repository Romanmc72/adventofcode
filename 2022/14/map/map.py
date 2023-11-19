#!/usr/bin/env python3
"""
Description
-----------
Helper module for containing all of the code for the map itself.
"""
from typing import Dict, List

from .coordinate import Coordinate, COORDINATE_KEY_DELIMITER
from .exceptions import MapIsFullOfSandError
from .logger import LOGGER
from .substance import Substance

SOURCE = Coordinate(500, 0, Substance.SOURCE)
STOPPERS = set([Substance.ROCK, Substance.SAND])


class Map:
    def __init__(
        self,
        coordinates: Dict[str, Coordinate] = None,
        sand_sources: List[Coordinate] = None,
    ) -> None:
        """
        Description
        -----------
        Creates the map out of either the array of arrays of coordinates or it
        uses an empty dict and can add coordinates later.
        """
        self.coordinates = coordinates or dict()
        self.sand_sources = sand_sources or []
        self.full = False

    def set_coordinate(self, coordinate: Coordinate) -> None:
        """Sets a coordinate on the map"""
        self.coordinates[coordinate.key] = coordinate

    def get_coordinate(self, x: int, y: int) -> Coordinate:
        """Gets a coordinate on the map"""
        return self.coordinates.get(
            Coordinate.coordinate_key(x, y), Coordinate(x, y, None)
        )

    @property
    def y_values(self) -> list:
        """Get all of the y values"""
        y_values = []
        coordinate_keys = self.coordinates.keys()
        for key in coordinate_keys:
            _, y = Coordinate.parse_key(key)
            y_values.append(y)
        return y_values

    @property
    def x_values(self) -> list:
        """Get all of the x values"""
        x_values = []
        coordinate_keys = self.coordinates.keys()
        for key in coordinate_keys:
            x, _ = Coordinate.parse_key(key)
            x_values.append(x)
        return x_values

    def __iter__(self):
        """Allows the map to be iterable"""
        x_values = self.x_values
        y_values = self.y_values
        self.min_x = min(x_values)
        self.max_x = max(x_values)
        self.min_y = min(y_values)
        self.max_y = max(y_values)
        self.x = self.min_x
        self.y = self.min_y
        return self

    def __next__(self):
        """Gets the next element in the map"""
        if self.y > self.max_y:
            raise StopIteration
        coordinate = self.get_coordinate(self.x, self.y)
        LOGGER.debug(
            f"retrieved {coordinate.substance} at {self.x}{COORDINATE_KEY_DELIMITER}{self.y}"
        )
        if self.x == self.max_x:
            self.x = self.min_x
            self.y += 1
        else:
            self.x += 1
        return coordinate

    def __fill_remainder_with_air(self) -> None:
        """
        Description
        -----------
        For the spaces inside to coordinate plane that have no occupying
        coordinate, this will set those to be the empty air value.
        """
        LOGGER.debug("Filling in the air!")
        for coordinate in self:
            if coordinate.substance is None:
                LOGGER.debug(
                    f"Setting {self.x}{COORDINATE_KEY_DELIMITER}{self.y} to {Substance.AIR}"
                )
                self.set_coordinate(
                    Coordinate(coordinate.x, coordinate.y, Substance.AIR)
                )

    def __str__(self) -> str:
        """Show the map as a string for printing out in the terminal"""
        current_y = None
        picture = []
        row = []
        for coordinate in self:
            if current_y is None:
                current_y = coordinate.y
            if coordinate.y != current_y:
                picture.append("".join(row))
                row = []
                current_y = coordinate.y
            row.append(coordinate.substance or Substance.AIR)
        picture.append("".join(row))
        return "\n".join(picture)

    def __add_line(self, start: Coordinate, end: Coordinate) -> None:
        """Adds a line of rock onto the map"""
        ordered_x = 1 if start.x <= end.x else -1
        ordered_y = 1 if start.y <= end.y else -1
        for x in range(start.x, end.x + (1 * ordered_x), ordered_x):
            for y in range(start.y, end.y + (1 * ordered_y), ordered_y):
                self.set_coordinate(Coordinate(x, y, Substance.ROCK))

    def __parse_line(self, input_line: str) -> None:
        """
        Description
        -----------
        From a line of input data, parse out what rock lines need to be added
        and add them.
        """
        coordinates = []
        coordinate_strings = input_line.split(" -> ")
        for coordinate_string in coordinate_strings:
            coordinate_pair = coordinate_string.split(COORDINATE_KEY_DELIMITER)
            x = int(coordinate_pair[0])
            y = int(coordinate_pair[1])
            coordinates.append(Coordinate(x, y, Substance.ROCK))
        for index, coordinate in enumerate(coordinates):
            try:
                self.__add_line(coordinate, coordinates[index + 1])
            except IndexError:
                pass

    def fill_map(self, input_data: List[str]) -> None:
        """Given the raw input data, produce the fill map"""
        # This is a given from the puzzle
        self.set_coordinate(SOURCE)
        for line in input_data:
            self.__parse_line(line)
        self.__fill_remainder_with_air()

    def drop_sand(self) -> None:
        """
        Description
        -----------
        Drop sand into the map from the sources coordinate.
        """
        if self.full:
            raise MapIsFullOfSandError("Cannot drop any more sand, we are full!")
        x = SOURCE.x
        y = SOURCE.y
        settled = False
        while not settled:
            below = self.get_coordinate(x, y + 1)
            below_left = self.get_coordinate(x - 1, y + 1)
            below_right = self.get_coordinate(x + 1, y + 1)
            LOGGER.debug(f"coordinate: ({x}, {y}) and")
            LOGGER.debug(f"{below.substance=}")
            LOGGER.debug(f"{below_left.substance=}")
            LOGGER.debug(f"{below_right.substance=}")
            if (
                below.substance in STOPPERS
                and below_left.substance in STOPPERS
                and below_right.substance in STOPPERS
            ):
                self.set_coordinate(Coordinate(x, y, Substance.SAND))
                settled = True
                if x == SOURCE.x and y == SOURCE.y:
                    self.full = True
            elif below.substance == Substance.AIR:
                y += 1
                continue
            elif below_left.substance == Substance.AIR:
                x -= 1
                continue
            elif below_right.substance == Substance.AIR:
                x += 1
                continue
            elif below.substance is None:
                if below.y == self.max_y + 2:
                    self.set_coordinate(Coordinate(below.x, below.y, Substance.ROCK))
                else:
                    self.set_coordinate(Coordinate(below.x, below.y, Substance.AIR))
                continue
            elif below_left.substance is None:
                if below.y == self.max_y + 2:
                    self.set_coordinate(Coordinate(below_left.x, below_left.y, Substance.ROCK))
                else:
                    self.set_coordinate(Coordinate(below_left.x, below_left.y, Substance.AIR))
                continue
            elif below_right.substance is None:
                if below.y == self.max_y + 2:
                    self.set_coordinate(Coordinate(below_right.x, below_right.y, Substance.ROCK))
                else:
                    self.set_coordinate(Coordinate(below_right.x, below_right.y, Substance.AIR))
                continue

    def clear_sand(self) -> None:
        """
        Description
        -----------
        Performs a reset of the map to clear out all of the sand
        """
        for coordinate in self:
            if coordinate.substance == Substance.SAND:
                self.set_coordinate(
                    Coordinate(coordinate.x, coordinate.y, Substance.AIR)
                )
        self.full = False

    @property
    def sand_count(self) -> int:
        """Get the total count of spaced filled by sand"""
        sand_count = 0
        for coordinate in self:
            if coordinate.substance == Substance.SAND:
                sand_count += 1
        return sand_count