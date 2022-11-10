import os

from othellot.models.othello import Board


class Cursor:
    """Defines a controllable cursor.

    This cursor can access a board, and a player controls a game using it.
    It is impossible for this cursor to be located out of the board.

    """
    def __init__(self, board: Board, row_number: int = 0,
                 column_number: int = 0) -> None:
        if not isinstance(board, Board):
            raise TypeError(
                f"'board' must be an instance of Board: {repr(board)}")
        self.board = board

        position = {"row": row_number, "column": column_number}
        for key in position:
            value = position.get(key)
            if not isinstance(value, int):
                raise TypeError(
                    f"'{key}_number' must be an integer: {repr(value)}")
        self.pos = self.position = position
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

        c_row, c_col = self.pos.values()
        d_row, d_col = compass.get(direction)

        self.pos["row"] = c_row + d_row
        self.pos["column"] = c_col + d_col
        self.clamp_itself_within_board()

    def clamp_itself_within_board(self) -> None:
        """Clamps this cursor within the board.

        This method clamps this cursor's position within the range of the
        board. The 'range' here means the bounding box defined by both the size
        of the board and its origin.

        """
        clamp = lambda x, minimum, maximum: max(minimum, min(x, maximum))

        c_row, c_col = self.pos.values()
        o_row, o_col = self.board.origin.values()
        b_width, b_height = self.board.width, self.board.height

        self.pos["row"] = clamp(c_row, o_row, b_height - o_row - 1)
        self.pos["column"] = clamp(c_col, o_col, b_width - o_col - 1)


def clear_console() -> None:
    """Clears the console."""
    command = "cls" if os.name == "nt" else "clear"
    os.system(command)


def convert_board_into_str(board: Board, cursor: Cursor) -> str:
    """Converts an instance of Board into a string.

    This function assigns each grid of the board, including a cursor, to a
    single character decorated by escape sequences. They are concatenated
    with spaces, returned as a representation of the board by this function.

    """
    if not isinstance(board, Board):
        raise TypeError(f"'board' must be an instance of Board: {repr(board)}")
    if not isinstance(cursor, Cursor):
        raise TypeError(
            f"'cursor' must be an instance of Cursor: {repr(cursor)}")

    mapping = {
        "none": [".", "blue"], "dark": ["D", "black"], "light": ["L", "white"],
        "unknown": ["?", "yellow"]
        }

    c_row, c_col = cursor.pos.values()

    product = ""
    for i in range(0, board.height):
        for j in range(0, board.width):
            grid = board.grids[i][j]
            try:
                packed_str = mapping[grid.state].copy()
            except KeyError:
                packed_str = mapping.get("unknown").copy()

            if (c_row, c_col) == (i, j):
                packed_str.append("bg_white")

            text = packed_str.pop(0)
            colors = packed_str

            product += colored_str(text, *colors)
            product += " "
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
