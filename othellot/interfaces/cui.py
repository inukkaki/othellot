import os

from othellot.models.othello import Board, Position


class Cursor:
    """Defines a controllable cursor.

    This cursor can access a board, and a player controls a game using it.
    It is impossible for this cursor to be located out of the board.

    """
    def __init__(self, board: Board, disk_color: str, row_number: int = 0,
                 column_number: int = 0) -> None:
        if not isinstance(board, Board):
            raise TypeError(
                f"'board' must be an instance of Board: {repr(board)}")
        self.board = board

        if not isinstance(disk_color, str):
            raise TypeError(
                f"'disk_color' must be a string: {repr(disk_color)}")
        disk_color_list = ["dark", "light"]
        if disk_color not in disk_color_list:
            raise ValueError(
                "Unsupported value. The value of 'disk_color' must be any one "
                f"of {', '.join(disk_color_list)}: {repr(disk_color)}")
        self.disk_color = disk_color

        try:
            self.pos = Position(row_number, column_number)
        except TypeError as err:
            raise TypeError(err) from None
        self.clamp_itself_within_board()

    def move(self, direction: str) -> None:
        """Moves this cursor's position within the bounds of the board.

        This method's argument ``direction`` is only allowed to receive an
        initial of 'north', 'south', 'east', or 'west'.

        """
        if not isinstance(direction, str):
            raise TypeError(f"'direction' must be a string: {repr(direction)}")
        compass = {"n": (-1, 0), "s": (1, 0), "e": (0, 1), "w": (0, -1)}
        if direction not in compass:
            raise ValueError(
                "Unsupported value. The value of 'direction' must be any one "
                f"of {', '.join(compass)}: {repr(direction)}")
        delta = Position(*(compass.get(direction)))
        self.pos += delta
        self.clamp_itself_within_board()

    def clamp_itself_within_board(self) -> None:
        """Clamps this cursor within the board.

        This method clamps this cursor's position within the range of the
        board. The 'range' here means the bounding box defined by both the size
        of the board and its origin.

        """
        clamp = lambda x, minimum, maximum: max(minimum, min(x, maximum))
        pos = self.pos
        origin = self.board.origin
        bd = self.board
        pos.row = clamp(pos.row, origin.row, bd.height + origin.row - 1)
        pos.col = clamp(pos.col, origin.col, bd.width + origin.col - 1)

    def place_a_disk(self) -> str:
        """Places the player's disk on the board."""
        pos = self.pos.to_tuple()
        status = self.board.flip_outflanked_disks(*pos, self.disk_color)
        return status


def clear_console() -> None:
    """Clears the console."""
    command = "cls" if os.name == "nt" else "clear"
    os.system(command)


def convert_board_into_str(cursor: Cursor, **kwargs) -> str:
    """Converts an instance of Board into a string.

    This function assigns each grid of a board where a passed cursor exists
    to a single character decorated by escape sequences. They are
    concatenated with spaces, returned as a representation of the board.

    There is an argument that ``**kwargs`` supports: ``show_neighbors``,
    which determines whether this function renders the neighbors of a grid
    pointed by the cursor; ``show_cursor``, which determines whether the
    cursor is rendered on the board.

    """
    if not isinstance(cursor, Cursor):
        raise TypeError(
            f"'cursor' must be an instance of Cursor: {repr(cursor)}")

    board = cursor.board

    mapping = {
        "none": [".", "blue"], "dark": ["D", "black"], "light": ["L", "white"],
        "available": ["*", "yellow"], "unknown": ["?", "yellow"]
    }

    # Obtain the neighborhood of a grid that the cursor points (optional)
    if kwargs.get("show_neighbors"):
        target_grid = board.grids[cursor.pos.row][cursor.pos.col]
        neighborhood = [
            (cursor.pos.row + i, cursor.pos.col + j)
            for i, j in target_grid.neighbors.keys()
        ]
    else:
        neighborhood = []

    product = ""
    for i in range(board.height):
        for j in range(board.width):
            grid = board.grids[i][j]
            try:
                packed_str = mapping[grid.state].copy()
            except KeyError:
                packed_str = mapping.get("unknown").copy()

            # Render the cursor
            if kwargs.get("show_cursor"):
                if (i, j) == cursor.pos.to_tuple():
                    packed_str.append("bg_white")

            # Render neighbors (optional)
            if (i, j) in neighborhood:
                packed_str.append("red")

            # Render expected captives
            if grid in board.expected_captives:
                packed_str.append("green")

            text = packed_str.pop(0)
            colors = packed_str
            product += (colored_str(text, *colors) + " ")
        product += "\n"

    return product


def colored_str(text: object, *colors: str) -> str:
    """Colors a string by using ANSI escape sequences.

    This function converts ``text`` into a string and gives color to it. The
    color configuration is provided by ``colors``. It is possible to pass as
    many colors as desired, but later ones take priority.

    """
    converted_text = text if isinstance(text, str) else repr(text)

    if len(colors) == 0:
        return converted_text

    mapping = {
        "black": 30, "red": 31, "green": 32, "yellow": 33, "blue": 34,
        "magenta": 35, "cyan": 36, "white": 37, "default": 39, "bg_black": 40,
        "bg_red": 41, "bg_green": 42, "bg_yellow": 43, "bg_blue": 44,
        "bg_magenta": 45, "bg_cyan": 46, "bg_white": 47, "bg_default": 49
    }

    color_codes = []
    for key in colors:
        if not isinstance(key, str):
            raise TypeError(f"'colors' must be passed strings: {repr(key)}")
        try:
            value = str(mapping[key])
        except KeyError:
            raise ValueError(f"Unsupported value: {repr(key)}") from None
        color_codes.append(value)
    reset_codes = [str(mapping.get("default")), str(mapping.get("bg_default"))]

    prefix = "\033["
    suffix = "m"
    delimiter = ";"

    head = prefix + delimiter.join(color_codes) + suffix
    bottom = prefix + delimiter.join(reset_codes) + suffix
    product = head + converted_text + bottom

    return product
