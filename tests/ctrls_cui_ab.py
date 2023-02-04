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

    board = Board(**size_of_board)
    board.linking()

    # Determine the color of disks of the player
    disk_color_list = ["dark", "light"]
    while True:
        value = input(f"which? (dark/light) {prompt} ")
        cause = colored_str(value, "black")
        if value not in disk_color_list:
            print(f"unsupported value: {cause}")
            continue
        players_disks = value
        break

    cursor = Cursor(board, players_disks)

    disk_color_permutation = {"dark": "light", "light": "dark"}

    # Prepare instances necessary for games
    render_option = {"show_neighbors": False}
    def reverse(key) -> None:
        render_option[key] = not render_option.get(key)

    func_dict = {
        "w": (cursor.move, ["n"]), "a": (cursor.move, ["w"]),
        "s": (cursor.move, ["s"]), "d": (cursor.move, ["e"]),
        "z": (cursor.place_a_disk, []), "n": (reverse, ["show_neighbors"])
    }

    # Main loop
    is_forced_to_quit = False

    board.setup()

    while True:
        board.suggest_available_grids(cursor.disk_color)

        message = f"operate ({cursor.disk_color})"
        while True:
            cursor_pos = cursor.pos.to_tuple()
            board.suggest_expected_captives(*cursor_pos, cursor.disk_color)

            # Update the console
            clear_console()
            print(convert_board_into_str(cursor, **render_option))

            # Receive an entry from the keyboard
            entry = input(f"{message} {prompt} ")
            if entry == "x":
                is_forced_to_quit = True
                break

            # Perform a function corresponded to the entry
            try:
                target_func, args_list = func_dict[entry]
                status = target_func(*args_list)
            except KeyError:
                pass

            # Break this loop when a disk is placed successfully
            if status == "succeeded in placing the disk":
                break

        # Quit the loop
        if is_forced_to_quit:
            break

        cursor.disk_color = disk_color_permutation.get(cursor.disk_color)

    return 0


sys.exit(main())
