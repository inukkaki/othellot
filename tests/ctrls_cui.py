"""A module for checking game controls in the CUI."""
import sys

from othellot.interfaces.cui import (
    clear_console,
    colored_str,
    convert_board_into_str,
    Cursor
    )
from othellot.models.othello import Board


def main() -> int:
    """Replicates the actual game flow."""
    clear_console()

    # determine the size of a board
    b_size = {"width": 8, "height": 8}
    for key in b_size:
        while True:
            raw_value = input(key + colored_str(" > ", "yellow"))
            try:
                value = int(raw_value)
            except ValueError:
                print("only integer allowed: "
                      f"{colored_str(raw_value, 'black')}")
                continue
            if value <= 0:
                print("must be greater than zeto: "
                      f"{colored_str(value, 'black')}")
                continue
            b_size[key] = value
            break

    # make instances
    board = Board(**b_size)
    cursor = Cursor(board)

    # display the board
    clear_console()
    print(convert_board_into_str(board, cursor))

    return 0


sys.exit(main())
