#!/usr/bin/env python3
"""
Part 1
------
If a tree is visible looking down/up a column or in/out of a row (meaning no
trees taller or as tall as it are in the row/column before it) then it is
visible! Also trees on the edge are visible by default.

Part 2
------
Now to calculate the "scenic score" which is the number of trees visible in a
given direction (left, right, up, or down) multiplied by the trees visible in
all of the other directions (so: left * right * up * down). Below is an
illustration of trees at various heights and their scenic score being
calculated for one dimension. The same technique can be used for all of the
other dimension because there is no unique property of a given dimension, only
that trees on the edges have a 0 for one of their scenic score inputs
(and 0 * anything = 0).

Scenic Scores:
<------------------------
0 1 1 3 1 1 1 1 4 9 1 2 1
###########################
                  ^
      ^ ^       ^ |   ^
  ^   | | ^     | |   |
  |   | | | ^   | |   |
^ | ^ | | | | ^ | | ^ | ^
| | | | | | | | | | | | |
###########################
Stepwise <Tree = (h=height, s=score)>:
^
First/shortest, add to stack [(h=1, s=0)]
+-^
Tallest! popleft, cumulate, add one [(h=2, s=1)]
+---^
Shorter, append. [(h=2, s=1), (h=1, s=1)]
+-----^
Tallest! popleft, cumulate, add one [(h=4, s=3)]
+-------^
Ties, tallest, cumulate popright, add one, append [(h=4, s=3), (h=4, s=1)] 
+---------^
Shorter, append. [(h=4, s=3), (h=4, s=1), (h=3, s=1)]
+-----------^
Shorter, append. [(h=4, s=3), (h=4, s=1), (h=3, s=1), (h=2, s=1)]
+-------------^
Shorter, append. [(h=4, s=3), (h=4, s=1), (h=3, s=1), (h=2, s=1), (h=1, s=1)]
+---------------^
Ties, tallest, cumulate popright, add one, append [(h=4, s=3), (h=4, s=1), (h=4, s=4)]
+---------------^
Tallest! popleft, cumulate, add one [(h=5, s=9)]
###########################
Looking the other direction...
------------------------>
1 2 1 1 4 3 2 1 1 3 1 1 0
###########################

"""
from collections import deque
from enum import Enum
from math import prod
from typing import List, Tuple

from input import get_data

MAX_HEIGHT = 9


class Direction(int, Enum):
    FORWARD = 1
    REVERSE = -1


class Tree:
    def __init__(
        self,
        height: int,
        coordinate: Tuple[int, int],
        is_visible: bool = False,
        scenic_score: int = 0,
        viewing_distances: List[int] = None,
    ) -> None:
        self.height = height
        self.coordinate = coordinate
        self.is_visible = is_visible
        self.scenic_score = scenic_score
        self.viewing_distances = viewing_distances or []

    def calculate_scenic_score(self) -> int:
        scenic_score = prod(self.viewing_distances)
        self.scenic_score = scenic_score
        return scenic_score


class TreeLine:
    """
    Description
    -----------
    Simply a line of trees! They can be considered a "row" or a "column" but
    the behavior is identical either way.

    Params
    ------
    :trees: List[Tree] = None
    The list of trees in the tree line. If None is provided, then an empty
    list will be used and the treeline can be populated later.
    """

    def __init__(self, trees: List[Tree] = None) -> None:
        self.trees = trees or []

    def check_visibility(self, direction: Direction) -> None:
        """
        Description
        -----------
        This will check to see whether or not all trees in the tree line are
        visible as well as calculate the viewing distance of every tree in the
        tree line for this given direction.

        Params
        ------
        :direction: Direction
        Whether or not to check this tree line from left to right (FORWARD)
        or from right to left (REVERSE).

        Return
        ------
        None
        """
        stack = deque()
        is_outermost = True
        start = 0 if direction == Direction.FORWARD else -1
        for tree in self.trees[start::direction]:
            if is_outermost:
                tree.viewing_distances.append(0)
                tree.is_visible = True
                is_outermost = False
                stack.append(tree)
            elif tree.height > stack[0].height:
                tree.is_visible = True
                self._collapse_stack(
                    stack=stack, comparer=tree, direction=Direction.FORWARD
                )
            elif tree.height > stack[-1].height:
                self._collapse_stack(
                    stack=stack, comparer=tree, direction=Direction.REVERSE
                )
            else:
                tree.viewing_distances.append(1)
                stack.append(tree)

    @staticmethod
    def _collapse_stack(
        stack: deque[Tree], comparer: Tree, direction: Direction
    ) -> None:
        """
        Description
        -----------
        Collapses a stack from one direction, using a tree to compare against
        the others within the stack. If the comparer tree is larger than the
        tree in the stack, then it will pop the tree off of the stack and
        compare to the next tree in the stack in that same direction until
        either the stack is empty or a larger tree is found, at which point
        the accumulated popped trees from the stack will have their latest
        viewing distances totaled and added onto the comparer, who will then
        be added to the stack at the position it was comparing against last.

        Params
        ------
        :stack: deque[Tree]
        The stack of trees to use for collapsing

        :comparer: Tree
        The tree we are currently comparing with

        :direction: Direction
        The direction we are collapsing the stack to. If FORWARD we go left to
        right if REVERSE we gor right to left.

        Return
        ------
        None
        """
        popper = stack.popleft if direction == Direction.FORWARD else stack.pop
        appender = stack.appendleft if direction == Direction.FORWARD else stack.append
        cumulative_viewing_distance = 0
        try:
            popped = popper()
            while popped.height < comparer.height:
                cumulative_viewing_distance += popped.viewing_distances[-1]
                popped = popper()
            if popped.height >= comparer.height:
                appender(popped)
        except IndexError:
            pass
        finally:
            comparer.viewing_distances.append(cumulative_viewing_distance + 1)
            appender(comparer)

    def check_both_directions(self) -> None:
        """Runs the visibility check in both directions on the tree line"""
        self.check_visibility(Direction.FORWARD)
        self.check_visibility(Direction.REVERSE)


class Matrix:
    def __init__(
        self, rows: List[TreeLine] = None, columns: List[TreeLine] = None
    ) -> None:
        self.rows = rows or []
        self.columns = columns or []
        self.visible_trees = 0
        self.best_visibility = 0

    def scan_forrest(self) -> None:
        for row in self.rows:
            row.check_both_directions()
        for column in self.columns:
            column.check_both_directions()

    def calculate_visibility(self) -> None:
        self.scan_forrest()
        for row in self.rows:
            for tree in row.trees:
                self.visible_trees += 1 if tree.is_visible else 0
                score = tree.calculate_scenic_score()
                if score > self.best_visibility:
                    self.best_visibility = score

    @classmethod
    def from_raw_data(cls, raw_data: List[str]):
        new_matrix = cls()
        x = 0
        y = 0
        for row in raw_data:
            new_matrix.rows.append(TreeLine())
            for height in row:
                if y == 0:
                    new_matrix.columns.append(TreeLine())
                tree = Tree(height=int(height), coordinate=(x, y))
                new_matrix.rows[y].trees.append(tree)
                new_matrix.columns[x].trees.append(tree)
                x += 1
            x = 0
            y += 1
        return new_matrix


def main():
    matrix = Matrix.from_raw_data(get_data())
    matrix.calculate_visibility()
    print(f"Looks like we can see a total of {matrix.visible_trees} trees.")
    print(f"And the best visibility has {matrix.best_visibility} scenic score.")


if __name__ == "__main__":
    main()
