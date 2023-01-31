"""A module for checking game controls in the CUI.

In this version this program receive input from the keyboard in a
sequential way.

"""
import sys

from othellot.interfaces.cui import (
    clear_console,
    colored_str,
    convert_board_into_str,
    Cursor
)
from othellot.models.othello import Board


def main() -> int:
    """A function for considering the actual game flow."""
    clear_console()
    prompt = colored_str(">", "yellow")

    # Determine the size of a board
    size_of_board = {"width": 8, "height": 8}
    for key in size_of_board:
        while True:
            raw_value = input(f"{key} {prompt} ")
            cause = colored_str(raw_value, "black")
            try:
                value = int(raw_value)
            except ValueError:
                print(f"only integer allowed: {cause}")
                continue
            if value <= 0:
                print(f"must be greater than zero: {cause}")
                continue
            size_of_board[key] = value
            break

    # Prepare instances necessary for games
    board = Board(**size_of_board)
    board.linking()
    board.setup()

    cursor = Cursor(board)

    render_option = {"show_neighbors": False}
    def reverse(key) -> None:
        render_option[key] = not render_option.get(key)

    func_dict = {
        "w": (cursor.move, ["n"]), "a": (cursor.move, ["w"]),
        "s": (cursor.move, ["s"]), "d": (cursor.move, ["e"]),
        "n": (reverse, ["show_neighbors"])
    }

    # Main loop
    message = "operate"

    while True:
        # Update the console
        clear_console()
        print(convert_board_into_str(cursor, **render_option))

        # Receive an entry from the keyboard
        entry = input(f"{message} {prompt} ")
        if entry == "x":
            break

        # Perform a function corresponded to the entry
        try:
            target_func, args_list = func_dict[entry]
            target_func(*args_list)
        except KeyError:
            pass

    return 0


sys.exit(main())
