from __future__ import annotations


class Grid:
    """Defines a grid that composes a board.

    The grid is arranged in a reticular pattern. A disk sits on the grid,
    and its state depends on the value of ``state``, which is an attribute
    of the grid.

    The grid can access its neighbor grids through ``neighbors``.

    """
    def __init__(self, r: int, c: int, state: str = "none") -> None:
        position = {"row": r, "column": c}
        for key in position:
            value = position.get(key)
            if not isinstance(value, int):
                raise TypeError(
                    f"'{key[0]}' must be an integer: {repr(value)}")
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

        relative_position = (
            neighbor.pos.get("row") - self.pos.get("row"),
            neighbor.pos.get("column") - self.pos.get("column"))
        self.neighbors[relative_position] = neighbor


class Board:
    """Defines a board to have games.

    The board controls its grids through ``grids`` attribute. It is a two-
    dimensional array of grids, and its size is determined by ``width`` and
    ``height``.

    """
    def __init__(self, width: int, height: int) -> None:
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

        self.grids = []
        for r in range(0, self.height):
            row = []
            for c in range(0, self.width):
                grid = Grid(r, c)
                row.append(grid)
            self.grids.append(row)
