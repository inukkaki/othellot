from __future__ import annotations
from math import ceil


class Position:
    """Defines a generic standard of position instances.

    This class supports a two-dimensional position, consisting of two
    integers ``row`` and ``col``.

    """
    def __init__(self, row_number: int, column_number: int) -> None:
        position = {"row": row_number, "column": column_number}
        for key in position:
            value = position.get(key)
            if not isinstance(value, int):
                raise TypeError(
                    f"'{key}_number' must be an integer: {repr(value)}")
        self.row, self.col = position.values()

    def __add__(self, other: Position) -> Position:
        if not isinstance(other, Position):
            raise TypeError(
                "Addition between Position instances is only supported: "
                f"{repr(other)}")
        s_row = self.row + other.row
        s_col = self.col + other.col
        summation = Position(s_row, s_col)
        return summation

    def __sub__(self, other: Position) -> Position:
        if not isinstance(other, Position):
            raise TypeError(
                "Subtraction between Position instances is only supported: "
                f"{repr(other)}")
        d_row = self.row - other.row
        d_col = self.col - other.col
        difference = Position(d_row, d_col)
        return difference

    def to_tuple(self) -> tuple[int, int]:
        """Returns a tuple consisting of ``row`` and ``col``."""
        return (self.row, self.col)


class Grid:
    """Defines a grid that composes a board.

    This grid is arranged in a reticular pattern. A disk sits on this grid,
    and its state depends on the value of ``state``, which is allowed to
    receive only specific words.

    This grid can access its neighbor grids through ``neighbors``.

    """
    def __init__(self, row_number: int, column_number: int,
                 state: str = "none") -> None:
        try:
            self.pos = Position(row_number, column_number)
        except TypeError as err:
            raise TypeError(err) from None
        self._state = self.state = state
        self.neighbors = {}

    @property
    def state(self) -> str:
        """The state of a disk sitting on this grid."""
        return self._state

    @state.setter
    def state(self, state: str) -> None:
        if not isinstance(state, str):
            raise TypeError(f"'state' must be a string: {repr(state)}")
        states_of_disks = ["none", "dark", "light"]
        if state not in states_of_disks:
            raise ValueError(
                "Unsupported value. The value of 'state' must be any one of "
                f"{', '.join(states_of_disks)}: {repr(state)}")
        self._state = state

    def add_neighbor(self, neighbor: Grid) -> None:
        """Adds a neighbor grid to this grid's list.

        The dictionary pairs the instance of the neighbor grid with its
        relative position. The former is a value, and the latter is a key. The
        neighbor grid does not necessarily border this grid.

        """
        if not isinstance(neighbor, Grid):
            raise TypeError(
                f"'neighbor' must be an instance of Grid: {repr(neighbor)}")
        relative_pos = neighbor.pos - self.pos
        self.neighbors[relative_pos.to_tuple()] = neighbor


class Board:
    """Defines a board to have a game.

    This board controls its grids through ``grids`` attribute. It can be
    used as a two-dimensional array of grids, and its size is determined by
    ``width`` and ``height``.

    """
    def __init__(self, width: int, height: int) -> None:
        self.origin = Position(0, 0)

        size = {"width": width, "height": height}
        for key in size:
            value = size.get(key)
            if not isinstance(value, int):
                raise TypeError(
                    f"'{key}' must be a positive integer: {repr(value)}")
            if value <= 0:
                raise ValueError(
                    f"'{key}' must be greater than zero: {repr(value)}")
        self.width = size.get("width")
        self.height = size.get("height")

        origin = self.origin

        self.grids = []
        for i in range(origin.row, self.height + origin.row):
            row = []
            for j in range(origin.col, self.width + origin.col):
                grid = Grid(i, j)
                row.append(grid)
            self.grids.append(row)

    def is_enclosing(self, row_number: int, column_number: int,
                     offsets: str | None = None) -> bool:
        """Checks if this board encloses passed integers as a point.

        The optional argument ``offsets`` determines whether the range of this
        board is considered with offset values added when calculating the
        return value. If it is equivalent to 'origin', the offset is the origin
        of this board; otherwise, nothing. Defaults to None.

        """
        position = {"row": row_number, "column": column_number}
        for key in position:
            value = position.get(key)
            if not isinstance(value, int):
                raise TypeError(
                    f"'{key}_number' must be an integer: {repr(value)}")
        origin = self.origin if offsets == "origin" else Position(0, 0)
        cond_row = (0 <= row_number - origin.row <= self.height - 1)
        cond_col = (0 <= column_number - origin.col <= self.width - 1)
        return cond_row and cond_col

    def setup(self) -> None:
        """Arranges disks in an initial placement.

        Ordinarily a disk with the light side is put on the northwest side of
        the center of a board, and then two darks and a light follow it one
        after the other.

        """
        # Calculate the center of this board
        c_row = ceil(self.height / 2) - 1
        c_col = ceil(self.width / 2) - 1

        domain = [(i, j) for i in range(2) for j in range(2)]
        mapping = {0: "light", 1: "dark"}
        for i, j in domain:
            try:
                grid = self.grids[c_row + i][c_col + j]
            except IndexError:
                continue
            state = mapping.get((i+j) % 2)
            grid.state = state
