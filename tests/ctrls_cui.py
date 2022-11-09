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

    prompt = colored_str("> ", "yellow")

    # Determine the size of a board
    b_size = {"width": 8, "height": 8}
    for key in b_size:
        while True:
            raw_value = input(f"{key} {prompt}")
            try:
                value = int(raw_value)
            except ValueError:
                print("only integer allowed: "
                      f"{colored_str(raw_value, 'black')}")
                continue
            if value <= 0:
                print("must be greater than zero: "
                      f"{colored_str(value, 'black')}")
                continue
            b_size[key] = value
            break

    # Get ready for a game
    board = Board(**b_size)
    board.setup()

    cursor = Cursor(board)

    # Main loop
    while True:
        message = "cursor"
        while True:
            # Display the board
            clear_console()
            print(convert_board_into_str(board, cursor))

            # Wait for an input to the cursor
            direction = input(f"{message} {prompt}")
            try:
                cursor.move(direction)
                break
            except ValueError:
                if direction == "z":
                    return 0
                message = "unsupported value; cursor"


sys.exit(main())
