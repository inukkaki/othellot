from __future__ import annotations


class Grid:
    """Defines a grid that composes a board.

    The grid is arranged in a reticular pattern. A disk sits on the grid,
    and its state depends on the value of ``state``, which is an attribute
    of the grid.

    The grid can access its neighbor grids through ``neighbors``.

    """
    def __init__(self, row_number: int, column_number: int,
                 state: str = "none") -> None:
        position = {"row": row_number, "column": column_number}
        for key in position:
            value = position.get(key)
            if not isinstance(value, int):
                raise TypeError(
                    f"'{key}_number' must be an integer: {repr(value)}")
        self.pos = self.position = position

        states_of_disk = ["none", "dark", "light"]
        if not isinstance(state, str):
            raise TypeError(f"'state' must be a string: {repr(state)}")
        if state not in states_of_disk:
            raise ValueError(
                "Unsupported value. The value of 'state' must be any one of "
                f"{', '.join(states_of_disk)}: {repr(state)}")
        self.state = state

        self.neighbors = {}

    def add_neighbor(self, neighbor: Grid) -> None:
        """Adds a neighbor grid to ``neighbors``.

        The dictionary pairs the instance of the neighbor grid with its
        relative position. The former is a value, and the latter is a key. The
        neighbor grid does not necessarily border this grid.

        """
        if not isinstance(neighbor, Grid):
            raise TypeError(
                f"'neighbor' must be an instance of Grid: {repr(neighbor)}")

        n_row, n_col = neighbor.pos.values()
        s_row, s_col = self.pos.values()
        relative_position = (n_row - s_row, n_col - s_col)

        self.neighbors[relative_position] = neighbor


class Board:
    """Defines a board to have games.

    The board controls its grids through ``grids`` attribute. It is a two-
    dimensional array of grids, and its size is determined by ``width`` and
    ``height``.

    """
    def __init__(self, width: int, height: int) -> None:
        self.origin = {"row": 0, "column": 0}

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

        o_row, o_col = self.origin.values()

        self.grids = []
        for i in range(o_row, self.height - o_row):
            row = []
            for j in range(o_col, self.width - o_col):
                grid = Grid(i, j)
                row.append(grid)
            self.grids.append(row)
