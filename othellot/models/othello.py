from __future__ import annotations


class Grid:
    """Defines a grid that composes a board.

    Args:
        r (int): The number of a row that includes the grid.
        c (int): The number of a column that includes the grid.
        state (str): The state of a disk on the grid. If the grid has no
            disks, this argument takes 'none'. Otherwise, 'dark' for a disk
            with the dark side, and 'light' for that with the light side.
            Defaults to 'none'.

    Attributes:
        position (dict[str, int]): The position of the grid on the board.
            Consists of the row number and the column number. Alias ``pos``.
        state (str): The state of a disk on the grid.
        neighbors (dict[tuple[int, int], Grid]): Stores the pointer to each
            neighbor grid. This dictionary makes each pointer correspond to
            the neighbor grid's relative position.

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
        """Adds a neighbor grid to the dictionary ``neighbors``.

        The neighbor grid instance is paired with its relative position. The
        former is a value, and the latter is a key.

        Args:
            neighbor: A neighbor grid instance. It is allowed no matter if it
                does not technically border the grid.

        """
        relative_position = (
            neighbor.pos.get("row") - self.pos.get("row"),
            neighbor.pos.get("column") - self.pos.get("column"))
        self.neighbors[relative_position] = neighbor


class Board:
    """Defines a board to play Othello.

    Args:
        width (int): The width of the board. The number of columns. A
            positive integer is only allowed.
        height (int): The height of the board. The number of rows. A
            positive integer is only allowed.

    Attributes:
        width (int): The width of the board. The number of columns.
        height (int): The height of the board. The number of rows.
        grids (list[list[Grid]]): A two-dimensional array of grids.

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
