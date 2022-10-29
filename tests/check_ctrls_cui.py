"""A module for checking game controls in the CUI."""
import os
import sys

from othellot.models.othello import Board
from othellot.interfaces.cui import convert_board_into_str, Cursor


def main() -> int:
    """The main function."""
    b_size = {"width": 8, "height": 8}
    for key in b_size:
        print(f"Enter the {key} of the board:")
        while True:
            raw_value = input("> ")
            try:
                value = int(raw_value)
            except ValueError:
                print(f"The '{key}' must be an integer. Enter again:")
                continue
            if value <= 0:
                print(f"The '{key}' must be greater than zero. Enter again:")
                continue
            b_size[key] = value
            break

    board = Board(*b_size.values())
    cursor = Cursor(board)

    clear_console()
    print(convert_board_into_str(board, cursor))

    return 0


def clear_console() -> None:
    """Clears the console."""
    command = "cls" if os.name == "nt" else "clear"
    os.system(command)


sys.exit(main())
