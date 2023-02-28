"""A module for checking game controls in the CUI.

This version uses pynput to receive input from the keyboard, and hence
the main loop runs in a continuous way.

"""
import getpass
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
    """A function for considering the actual game flow."""
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
    board.linking()

    cursor = Cursor(board)

    # Prepare for a keyboard listener
    escape_key = keyboard.Key.esc
    key_count = {"enter": 0}

    kbd_entry = {}
    def on_press(key) -> None | bool:
        try:
            dict_key = key.char
        except AttributeError:
            dict_key = key
            # Count the number of times the enter key is pressed
            if key == keyboard.Key.enter:
                key_count["enter"] += 1
        try:
            kbd_entry[dict_key] += 1
        except KeyError:
            kbd_entry[dict_key] = 1
        # If ``escape_key`` is pressed, terminate the listener
        if key == escape_key:
            return False
    def on_release(key) -> None:
        try:
            try:
                kbd_entry[key.char] = 0
            except AttributeError:
                kbd_entry[key] = 0
        except KeyError:
            pass
    kbd_entry_prev = None

    func_dict = {
        "w": (cursor.move, "n"), "a": (cursor.move, "w"),
        "s": (cursor.move, "s"), "d": (cursor.move, "e")
    }
    rendering_dict = {"n": {"show_neighbors": True}}

    # Start the keyboard listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    # Main loop
    fps = 30
    suspension_time = 1 / fps

    while True:
        # If the keyboard listener is not alive, break the loop
        if not listener.is_alive():
            break

        # Capture the keyboard entry on another dictionary
        kbd_entry_locked = kbd_entry.copy()

        # Check whether the keyboard entry is changed
        if kbd_entry_prev != kbd_entry_locked:
            rendering_option = {}

            # Perform a corresponding processing for each key entered
            for entered_key in kbd_entry_locked:
                if kbd_entry_locked.get(entered_key) == 0:
                    continue

                # Get a corresponding function
                try:
                    target_func, mapped_value = func_dict[entered_key]
                    target_func(mapped_value)
                except KeyError:
                    pass

                # Add a corresponding option for rendering the board
                try:
                    rendering_option |= rendering_dict[entered_key]
                except KeyError:
                    pass

            # Update the console
            clear_console()
            print(convert_board_into_str(cursor, **rendering_option))
            kbd_entry_prev = kbd_entry_locked.copy()

        time.sleep(suspension_time)

    clear_console()

    # Prevent the events from propagating themselves to the terminal
    for _ in range(key_count.get("enter")):
        _ = getpass.getpass(prompt="")
    clear_console()

    # NOTE: The Esc key clears characters on the prompt line in a console, at
    # least in PowerShell.

    return 0


sys.exit(main())
