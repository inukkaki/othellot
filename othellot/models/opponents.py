from othellot.models.othello import Board


class BaseOpponent:
    """Defines the base class of every opponent in the game."""
    def __init__(self, board: Board, disk_color: str) -> None:
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
