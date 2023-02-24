"""A module for checking game controls in the CUI.

Including a computer opponent...

"""
import sys
import threading
import time

from othellot.interfaces.cui import (
    clear_console,
    colored_str,
    convert_board_into_str,
    Cursor
)
import othellot.models.agents as agents
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
    opponents_disk = disk_color_permutation.get(players_disks)
    agent = agents.Kijitora(board, opponents_disk)

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

        # Player's turn
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
                if target_func == cursor.place_a_disk:
                    status = target_func(*args_list)
                else:
                    target_func(*args_list)
                    status = None
            except KeyError:
                status = None

            # Break this loop when a disk is placed successfully
            if status == "succeeded in placing the disk":
                clear_console()
                print(convert_board_into_str(cursor, **render_option))
                print("You placed a disk.")
                time.sleep(2.0)
                break

        # Quit the loop
        if is_forced_to_quit:
            break

        # Opponent's turn
        board.suggest_available_grids(agent.disk_color)
        clear_console()
        print(convert_board_into_str(cursor, **render_option))

        thread = threading.Thread(target=agent.start)
        thread.start()

        start_time = time.time()
        while True:
            current_time = time.time()
            delta_time = current_time - start_time
            if not thread.is_alive() and delta_time > 2.0:
                break
            time.sleep(0.0333)

        status = agent.place_a_disk()
        match status:
            case "succeeded in placing the disk":
                message = "Opponent placed a disk."
            case "target_grid is not a grid":
                board.clear_available_grids()
                message = "Opponent did not place a disk."
            case _:
                board.clear_available_grids()
                message = "Some kind of errors could have occurred."
        clear_console()
        print(convert_board_into_str(cursor, **render_option))
        print(message)
        time.sleep(2.0)

    return 0


sys.exit(main())
