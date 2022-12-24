"""A module for testing to monitor the keyboard."""
import sys
import time

from pynput import keyboard

from othellot.interfaces.cui import clear_console


def main() -> int:
    """A short procedure for testing to monitor the keyboard."""
    entry = {"current": None, "previous": None}

    def on_press(key) -> None:
        try:
            entered_key = key.char
            entry["previous"] = entry.get("current")
            entry["current"] = entered_key
        except AttributeError:
            pass

    # Start a keyboard listener
    listener = keyboard.Listener(on_press=on_press, suppress=True)
    listener.start()

    # NOTE: The boolean ``suppress``, which is a parameter of
    # ``keyboard.Listener``, prevents contents of the standard input buffer
    # flushing after this program terminates. However, please make sure that
    # the suppression does not apply only to the console where the interpreter
    # went live, but extends over all the other applications.

    # Main loop
    spf = 0.0333  # Stands for seconds per frame

    clear_console()
    print("If 'x' pressed, this program terminates.")

    while True:
        if entry["current"] == 'z':
            break

        # If a different key is pressed, the console updates itself
        if entry["current"] != entry["previous"]:
            clear_console()
            print(f"current: {repr(entry.get('current'))}")
            print(f"previous: {repr(entry.get('previous'))}")
            entry["previous"] = entry.get("current")

        time.sleep(spf)

    # Terminate the listener
    listener.stop()

    return 0


sys.exit(main())
