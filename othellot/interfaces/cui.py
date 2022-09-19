from othellot.models.othello import Board


class Cursor:
    """Defines a controllable cursor.

    This cursor can access a board, and a player controls a game using it.

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

    def clamp_itself_within_board(self) -> None:
        """Clamps this cursor within the board.

        This function clamps this cursor's position within the range of the
        board. The 'range' here means the bounding box defined by both the size
        of the board and its origin.

        """
        clamp = lambda x, minimum, maximum: max(minimum, min(x, maximum))

        c_row, c_col = self.pos.values()
        o_row, o_col = self.board.origin.values()
        b_width, b_height = self.board.width, self.board.height

        self.pos["row"] = clamp(c_row, o_row, b_height - o_row - 1)
        self.pos["column"] = clamp(c_col, o_col, b_width - o_col - 1)


def convert_board_into_str(board: Board, cursor: Cursor) -> str:
    """Converts an instance of Board into a string."""
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

            product += colored_str(packed_str)
            product += " "
        product += "\n"

    return product


def colored_str(packed_str: str | list[str]) -> str:
    """Colors a string by using ANSI escape sequences.

    The first item of ``packed_str`` is handled as a string that is supposed
    to be colored, and succeeding items are the color configuration of the
    string. It is possible to pass as many colors as desired, but latest
    ones take priority.

    """
    if isinstance(packed_str, str):
        return packed_str
    if not isinstance(packed_str, list):
        raise TypeError(
            "'packed_str' must be a string or a list of strings: "
            f"{repr(packed_str)}")

    try:
        text = packed_str[0]
    except IndexError:
        raise ValueError(
            "'packed_str' must have one or more string items. The first item "
            "is a string to color: " f"{repr(packed_str)}") from None
    if not isinstance(text, str):
        raise TypeError(
            "The first item of 'packed_str' must be a string; it is a string "
            "to color: " f"{repr(packed_str)}")
    if len(packed_str) == 1:
        return text

    mapping = {
        "black": 30, "red": 31, "green": 32, "yellow": 33, "blue": 34,
        "magenta": 35, "cyan": 36, "white": 37, "default": 39, "bg_black": 40,
        "bg_red": 41, "bg_green": 42, "bg_yellow": 43, "bg_blue": 44,
        "bg_magenta": 45, "bg_cyan": 46, "bg_white": 47, "bg_default": 49
        }

    properties = []
    for index in range(1, len(packed_str)):
        key = packed_str[index]
        try:
            value = str(mapping[key])
        except KeyError:
            raise ValueError(f"Unsupported value: {repr(key)}") from None
        properties.append(value)
    reset_codes = [str(mapping["default"]), str(mapping["bg_default"])]

    prefix = "\033["
    suffix = "m"

    delimiter = ";"
    head = prefix + delimiter.join(properties) + suffix
    bottom = prefix + delimiter.join(reset_codes) + suffix

    product = head + text + bottom
    return product
