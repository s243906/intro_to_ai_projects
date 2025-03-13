"""
Player module for the Kalaha game.
"""

from abc import ABC, abstractmethod
from board import KalahaBoard

class Player(ABC):
    """
    Abstract player interface for the Kalaha game.
    """
    @abstractmethod
    def get_move(self, board: KalahaBoard, player_id: int) -> int:
        """
        Return the pit index for the next move.
        """
        pass

class HumanPlayer(Player):
    """
    Implementation of a human player.
    """
    def get_move(self, board: KalahaBoard, player_id: int) -> int:
        """
        Get move from user input.
        """
        while True:
            try:
                pit = int(input(f"Player {player_id}, choose a pit: "))
                return pit
            except ValueError:
                print("Please enter a valid number.")