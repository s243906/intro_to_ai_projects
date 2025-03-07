"""
Game controller module for Kalaha game.
"""

from board import KalahaBoard
from rules import KalahaRules
from display import KalahaDisplay

class KalahaGame:
    """
    Game simulation class. 
    Definitions:
    - pit = whole 
    - stone = marbell
    - store = the wholes on the edges, where stones are collected 
    """
    def __init__(self, pits_per_player: int = 6, stones_per_pit: int = 4):
        """ Initialize a new Kalaha game. """
        self.board = KalahaBoard(pits_per_player, stones_per_pit)
        self.current_player = 0  # Player 0 starts
        self.display = KalahaDisplay()
    
    def is_move_valid(self, player: int, pit: int) -> bool:
        """ Check if a move is valid. """
        return KalahaRules.is_move_valid(self.board, player, pit)
    
    def move(self, player: int, pit: int) -> bool:
        """ Make a move in the game. Returns if player gets another turn. """
        return KalahaRules.make_move(self.board, player, pit)
    
    def is_game_over(self) -> bool:
        """ Check if the game is over. """
        return KalahaRules.is_game_over(self.board)
    
    def finish_game(self) -> None:
        """ Finalize the game by moving remaining stones to respective stores. """
        KalahaRules.finish_game(self.board)
    
    def get_winner(self) -> int:
        """ Get the winner of the game. """
        return KalahaRules.get_winner(self.board)
    
    def print_board(self) -> None:
        """ Print the current board state. """
        self.display.print_board(self.board)
    
    def print_game_over(self) -> None:
        """ Print game over message. """
        winner = self.get_winner()
        self.display.print_game_over(self.board, winner)