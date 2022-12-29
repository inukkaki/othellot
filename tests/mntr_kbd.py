"""A module for testing to monitor the keyboard."""
import copy
import getpass
import sys
import time

from pynput import keyboard

from othellot.interfaces.cui import clear_console


def main() -> int:
    """A short procedure for testing to monitor the keyboard."""
    key_count = {"enter": 0}
    escape_key = keyboard.Key.esc

    kbd_entry = set()
    def on_press(key) -> None | bool:
        try:
            kbd_entry.add(key.char)
        except AttributeError:
            kbd_entry.add(key)
            # Count the number of times the enter key is pressed
            if key == keyboard.Key.enter:
                key_count["enter"] += 1
        # If ``escape_key`` is pressed, terminate the listener
        if key == escape_key:
            return False
    def on_release(key) -> None:
        try:
            try:
                kbd_entry.remove(key.char)
            except AttributeError:
                kbd_entry.remove(key)
        except KeyError:
            pass
    kbd_entry_prev = copy.deepcopy(kbd_entry)

    # Start a keyboard listener
    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener.start()

    # NOTE: The boolean ``suppress``, which is a parameter of
    # ``keyboard.Listener``, prevents contents of the standard input buffer
    # flushing after this program terminates. However, please make sure that
    # the suppression does not apply only to the console where the interpreter
    # went live, but extends over all the other applications.

    # Main loop
    spf = 0.0333  # Stands for seconds per frame

    clear_console()
    print("If Esc is pressed, this program terminates itself.")

    while True:
        # Update the console
        if kbd_entry_prev != kbd_entry:
            clear_console()
            print([element for element in kbd_entry])
            kbd_entry_prev = copy.deepcopy(kbd_entry)

        # If the keyboard listener is not alive, break the loop
        if not listener.is_alive():
            break

        time.sleep(spf)

    clear_console()

    # Prevent the events from propagating themselves to the terminal
    for _ in range(key_count.get("enter")):
        _ = getpass.getpass(prompt="")
    clear_console()

    # The block above is a compromise to avoid propagating events that a user
    # input while the keyboard listener running, to the terminal. This works
    # but is not an official solution. If a better idea comes to mind, this
    # might be replaced with it.

    return 0


sys.exit(main())
