"""A module for checking game controls in the CUI."""
import sys
import time

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

    # Create instances necessary for a game
    board = Board(**b_size)
    board.setup()

    cursor = Cursor(board)

    # Prepare for a keyboard listener
    kbd_entry = {"key": None, "is_updated": False}
    def on_press(key) -> None:
        try:
            kbd_entry["key"] = key.char
            kbd_entry["is_updated"] = True
        except AttributeError:
            pass
    kbd_mapping = {
        "w": (cursor.move, "n"), "a": (cursor.move, "w"),
        "s": (cursor.move, "s"), "d": (cursor.move, "e")
    }

    # Main loop
    spf = 0.0333  # Stands for seconds per frame

    clear_console()
    print(convert_board_into_str(board, cursor))

    listener = keyboard.Listener(on_press=on_press, suppress=True)
    listener.start()

    while True:
        if kbd_entry["key"] == "z":
            break

        # The console updates itself if a different key is pressed
        if kbd_entry["is_updated"] == True:
            try:
                key = kbd_entry.get("key")
                target_func, mapped_value = kbd_mapping[key]
            except KeyError:
                pass
            else:
                target_func(mapped_value)
                kbd_entry["is_updated"] = False
                clear_console()
                print(convert_board_into_str(board, cursor))

        time.sleep(spf)

    listener.stop()


sys.exit(main())
