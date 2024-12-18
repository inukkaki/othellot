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
        states_of_disks = ["none", "dark", "light", "available"]
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
        self.domain = [
            (i, j) for i in range(self.height) for j in range(self.width)
        ]

        origin = self.origin

        self.grids = []
        for i in range(origin.row, self.height + origin.row):
            row = []
            for j in range(origin.col, self.width + origin.col):
                grid = Grid(i, j)
                row.append(grid)
            self.grids.append(row)

        self.available_grids = set()
        self.expected_captives = set()

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

    def is_consist_of(self, row_number: int, column_number: int) -> bool:
        """Checks if a tuple of passed integers belongs to the domain.

        This method does not check type of arguments strictly. If any but
        integers are passed, this returns False.

        """
        return (row_number, column_number) in self.domain

    def linking(self) -> None:
        """Links each grid of this board with its neighbor grids.

        Here 'neighbor grids' mean ones visually next to a targeted grid. The
        grids on the edge of this board hence have no neighbors out of the
        range of this board.

        """
        neighborhood = [
            (i, j) for i in range(-1, 2) for j in range(-1, 2)
            if (i != 0) or (j != 0)
        ]
        for i, j in self.domain:
            grid = self.grids[i][j]
            for k, l in neighborhood:
                n_row, n_col = i + k, j + l
                if not self.is_consist_of(n_row, n_col):
                    continue
                neighbor = self.grids[n_row][n_col]
                grid.add_neighbor(neighbor)

    def setup(self) -> None:
        """Arranges disks in an initial placement.

        Ordinarily a disk with the light side is put on the northwest side of
        the center of a board, and then two darks and a light follow it one
        after the other.

        """
        for i, j in self.domain:
            grid = self.grids[i][j]
            grid.state = "none"

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

    def clear_available_grids(self) -> None:
        """Backs down on the suggestion about available grids."""
        for i, j in self.domain:
            grid = self.grids[i][j]
            if grid.state == "available":
                grid.state = "none"
        self.available_grids.clear()

    def suggest_available_grids(self, client: str) -> int:
        """Suggests grids whose state is 'available'.

        The argument ``client`` must be the color of disks of a player that
        would like to know where available grids are. This method turns
        potential grids into available ones and returns the number of them;
        make sure that the number also includes the already-existing available
        grids on this board.

        """
        if not isinstance(client, str):
            raise TypeError(f"'client' must be a string: {repr(client)}")
        disk_color_list = ["dark", "light"]
        if client not in disk_color_list:
            raise ValueError(
                "Unsupported value. The value of 'client' must be any one of "
                f"{', '.join(disk_color_list)}: {repr(client)}")
        disk_color_permutation = {"dark": "light", "light": "dark"}
        opponent = disk_color_permutation.get(client)

        number_of_available_grids = 0

        neighborhood = [
            (i, j) for i in range(-1, 2) for j in range(-1, 2)
            if (i != 0) or (j != 0)
        ]
        for i, j in self.domain:
            grid = self.grids[i][j]
            if grid.state != "none":
                if grid.state == "available":
                    number_of_available_grids += 1
                    self.available_grids.add(grid)
                continue
            for k, l in neighborhood:
                if self.calculate_captives(client, opponent, grid, (k, l)):
                    grid.state = "available"
                    number_of_available_grids += 1
                    self.available_grids.add(grid)
                    break

        return number_of_available_grids

    def clear_expected_captives(self) -> None:
        """Clears elements of the expected captives."""
        self.expected_captives.clear()

    def suggest_expected_captives(self, row_number: int, column_number: int,
                                  client: str) -> None:
        """Updates elements of the expected captives.

        This method calculates opponent disks between the cursor and a client
        disk and adds them in ``expected_captives``. If failing to get a grid
        that the cursor sits on, this does nothing at all.

        """
        if not self.is_consist_of(row_number, column_number):
            return
        grid = self.grids[row_number][column_number]

        if not isinstance(client, str):
            raise TypeError(f"'client' must be a string: {repr(client)}")
        disk_color_list = ["dark", "light"]
        if client not in disk_color_list:
            raise ValueError(
                "Unsupported value. The value of 'client' must be any one of "
                f"{', '.join(disk_color_list)}: {repr(client)}")
        disk_color_permutation = {"dark": "light", "light": "dark"}
        opponent = disk_color_permutation.get(client)

        self.expected_captives.clear()
        if grid.state != "available":
            return

        neighborhood = [
            (i, j) for i in range(-1, 2) for j in range(-1, 2)
            if (i != 0) or (j != 0)
        ]
        for i, j in neighborhood:
            opp_set = self.calculate_captives(client, opponent, grid, (i, j))
            self.expected_captives.update(opp_set)

    def calculate_captives(self, client: str, opponent: str, grid: Grid,
                           direction: tuple[int, int]) -> set[Grid]:
        """Calculates opponents between two clients and returns their set.

        The argument ``grid`` is a Grid instance that the calculation is to
        start, and ``direction`` is a tuple of two integers that indicate the
        direction of the process. If they do not fulfill appropriate types and
        values, this method returns an empty set.

        """
        in_between_opponents = set()

        if not isinstance(grid, Grid):
            return in_between_opponents
        try:
            if len(direction) != 2:
                return in_between_opponents
        except TypeError:
            return in_between_opponents

        checked_grids = {grid}

        i, j = direction
        target_grid = grid
        while True:
            try:
                neighbor = target_grid.neighbors[(i, j)]
                if neighbor in checked_grids:
                    in_between_opponents.clear()
                    break
            except KeyError:
                in_between_opponents.clear()
                break
            checked_grids.add(neighbor)
            if neighbor.state == opponent:
                in_between_opponents.add(neighbor)
                target_grid = neighbor
                continue
            elif neighbor.state == client:
                break
            in_between_opponents.clear()
            break

        return in_between_opponents

    def flip_outflanked_disks(self, row_number: int, column_number: int,
                              client: str) -> str:
        """Turns outflanked disks' color into client's one.

        To be exact, this method places client's disk on a specified grid,
        turns current expected captives' color into client's one, and returns a
        string that indicates whether these processes are successfully done or
        failed, as a status. If the specified grid's state is not 'available',
        the disk will not be placed there.

        """
        status_f = "failed to place the disk"
        status_s = "succeeded in placing the disk"

        if not self.is_consist_of(row_number, column_number):
            return status_f
        grid = self.grids[row_number][column_number]
        if grid.state != "available":
            return status_f

        grid.state = client
        for target_grid in self.expected_captives:
            target_grid.state = client
        self.clear_available_grids()
        self.clear_expected_captives()

        return status_s
