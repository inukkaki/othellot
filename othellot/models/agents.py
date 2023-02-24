from othellot.models.othello import Board, Grid


class BaseAgent:
    """Defines the base class of every agent.

    An agent acts as a decision-making function of a player; that is, the
    agent decides a specified grid where the player should place a disk and
    conveys it to the board. It is sorely expected to be used for modeling
    the behavior of a non-playable character in this game.

    """
    def __init__(self, board: Board, disk_color: str) -> None:
        if not isinstance(board, Board):
            raise TypeError(
                f"'board' must be an instance of Board: {repr(board)}")
        self.board = board

        if not isinstance(disk_color, str):
            raise TypeError(
                f"'disk_color' must be a string: {repr(disk_color)}")
        disk_color_list = ["dark", "light"]
        if disk_color not in disk_color_list:
            raise ValueError(
                "Unsupported value. The value of 'disk_color' must be any one "
                f"of {', '.join(disk_color_list)}: {repr(disk_color)}")
        self.disk_color = disk_color

        self.target_grid = None
        self.state = "free"

    def consider_next_move(self) -> None:
        """Decides a specified grid where the player should place a disk.

        This is the core of the decision-making of this agent. You may override
        this method in a subclass to adjust the behavior of the player.

        """
        pass

    def start(self) -> None:
        """Starts to consider this agent's next move.

        This method is supposed to be passed to a separate thread as a callable
        object. This agent gets busy while this method running.

        """
        self.state = "busy"
        self.target_grid = self.consider_next_move()
        self.state = "free"

    def place_a_disk(self) -> str:
        """Places the player's disk on the board.

        This method requests the board to flip a disk on a grid targeted by
        this agent and returns a status. If this agent is busy or the targeted
        grid is not exist, this process fails.

        """
        status_f1 = "still busy"
        status_f2 = "target_grid is not a grid"
        if self.state == "busy":
            return status_f1
        if not isinstance(self.target_grid, Grid):
            return status_f2
        pos = self.target_grid.pos.to_tuple()
        status = self.board.flip_outflanked_disks(*pos, self.disk_color)
        return status


class Kijitora(BaseAgent):
    def consider_next_move(self) -> None:
        ...
