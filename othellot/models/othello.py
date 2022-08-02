class Grid:
    """Defines a grid that composes a board.

    Args:
        r (int): The number of a row that includes the grid.
        c (int): The number of a column that includes the grid.

    Attributes:
        position (dict[str, int]): The position of the grid on the board.
            Consists of the row number and the column number.

    """
    def __init__(self, r: int, c: int) -> None:
        position = {"row": r, "column": c}
        for key in position:
            value = position.get(key)
            if not isinstance(value, int):
                raise TypeError(
                    f"'{key[0]}' must be an integer: {repr(value)}")
        self.position = position
