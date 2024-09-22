from typing import List, Literal

from chrome_trex.core.multi_dino_game import MultiDinoGame


class DinoGame(MultiDinoGame):
    """
    A class that extends the MultiDinoGame class to manage a single-player game of
      T-Rex Rush.
    """

    def __init__(self, fps: int = 60, max_game_speed: int = 12):
        """
        Initialize the single-player game with given FPS and maximum game speed.

        Set fps to zero so the game goes at the maximum fps possible.

        Args:
            fps (int, optional): Frames per second for the game. Defaults to 60.
            max_game_speed (int, optional): Maximum game speed. Defaults to 12.
        """
        super().__init__(1, fps, max_game_speed)

    def step(self, action: Literal[0, 1, 2]) -> None:
        """
        Execute a single game step for the player dinosaur based on the provided action.

        Args:
            action (int): The action for the dinosaur
                (e.g., ACTION_FORWARD, ACTION_UP, ACTION_DOWN = 0, 1, 2).

        Returns:
            None
        """
        return super().step([action])

    def get_score(self) -> int:
        """
        Get the current score of the single player dinosaur.

        Returns:
            int: The score of the player dinosaur.
        """
        return self.get_scores()[0]

    def get_state(self) -> List[float]:
        """
        Get the current game state for the player dinosaur.

        The state consists of 10 values for the dinosaur:
            [DY, X1, Y1, H1, W1, X2, Y2, H2, W2, GS]
            DY: Distance in Y of the dinosaur.
            X1, Y1: Distance in X and Y from the first closest obstacle.
            H1: Height of the first closest obstacle.
            X2, Y2: Distance in X and Y from the second closest obstacle.
            H2: Height of the second closest obstacle.
            GS: Game speed.

        Returns:
            list: A list of 10 values representing the game state for the player
                    dinosaur.
        """
        return super().get_state()[0]
