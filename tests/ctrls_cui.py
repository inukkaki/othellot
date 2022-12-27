"""A module for checking game controls in the CUI."""
import sys

from pynput import keyboard

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

    # Determine the size of a board
    prompt = colored_str("> ", "yellow")

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

    # Create instances necessary for a game
    board = Board(**b_size)
    board.setup()

    cursor = Cursor(board)

    # Prepare for a keyboard listener
    escape_key = keyboard.Key.esc

    kbd_entry = [None]
    def on_press(key) -> bool:
        try:
            kbd_entry[0] = key.char
        except AttributeError:
            kbd_entry[0] = key
        return False
    kbd_mapping = {
        "w": (cursor.move, "n"), "a": (cursor.move, "w"),
        "s": (cursor.move, "s"), "d": (cursor.move, "e")
    }

    # Main loop
    while True:
        # Update the console
        clear_console()
        print(convert_board_into_str(board, cursor))

        # Receive an input from the keyboard
        with keyboard.Listener(on_press=on_press) as listener:
            listener.join()
        if kbd_entry[0] == escape_key:
            break

        # NOTE: The Esc key clears characters on the prompt line in a console,
        # at least in PowerShell.

        try:
            key = kbd_entry[0]
            target_func, mapped_value = kbd_mapping[key]
        except KeyError:
            pass
        else:
            target_func(mapped_value)
        kbd_entry = [None]

    return 0


sys.exit(main())
