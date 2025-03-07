# board.py
"""
Board module for Kalaha game.
"""

from typing import Tuple, List

class KalahaBoard:
    """
    Board representation for Kalaha game.
    """
    def __init__(self, pits_per_player: int = 6, stones_per_pit: int = 4):
        """ Initialize a new Kalaha board. """
        self.pits_per_player = pits_per_player
        self.total_pits = pits_per_player * 2 + 2  # with stores
        self.player_stores = [pits_per_player, pits_per_player * 2 + 1]  # indices for players 0 and 1
        self.board, self.current_player = self._init_board(stones_per_pit)
    
    def _init_board(self, stones_per_pit: int) -> Tuple[List[int], int]:
        """ Initialize the game board and starting player. """
        board = []

        # iterate through the pits, put stones (unless it's a store)
        for i in range(self.total_pits):
            if i in self.player_stores:  
                board.append(0)
            else:
                board.append(stones_per_pit)
                
        return board, 0  # Player 0 starts
    
    def get_player_pits(self, player: int) -> List[int]:
        """ Get the indices of pits owned by a player (excluding store). """
        if player == 0:
            return list(range(0, self.pits_per_player))
        else:
            return list(range(self.pits_per_player + 1, self.player_stores[1]))
    
    def get_store(self, player: int) -> int:
        """ Get the store index for a player. """
        return self.player_stores[player]
    
    def get_stones(self, pit: int) -> int:
        """ Get the number of stones in a pit. """
        return self.board[pit]
    
    def set_stones(self, pit: int, stones: int) -> None:
        """ Set the number of stones in a pit. """
        self.board[pit] = stones
    
    def add_stones(self, pit: int, stones: int) -> None:
        """ Add stones to a pit. """
        self.board[pit] += stones
    
    def get_opposite_pit(self, pit: int) -> int:
        """ Get the index of the pit opposite to the given pit. """
        return self.total_pits - 2 - pit