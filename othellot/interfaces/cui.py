from othellot.models.othello import Board


def convert_board_into_str(board: Board) -> str:
    """Converts an instance of Board into a string."""
    product = ""

    mapping = {"none": ".", "dark": "D", "light": "L", "unknown": "?"}

    for i in range(0, board.height):
        for j in range(0, board.width):
            grid = board.grids[i][j]
            try:
                char = mapping[grid.state]
            except KeyError:
                char = mapping.get("unknown")
            product += char
            product += " "
        product += "\n"

    return product
