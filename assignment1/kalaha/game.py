"""
Game controller module for Kalaha game.
"""

from typing import List
from board import KalahaBoard
from rules import KalahaRules
from display import KalahaDisplay
from player import Player

class KalahaGame:
    """
    Game simulation class. 
    Definitions:
    - pit = whole 
    - stone = marbell
    - store = the wholes on the edges, where stones are collected 
    """
    def __init__(self, players: List[Player], pits_per_player: int = 6, stones_per_pit: int = 4):
        """ Initialize a new Kalaha game with specified players. """
        self.board = KalahaBoard(pits_per_player, stones_per_pit)
        self.current_player = 0  # player 0 starts
        self.display = KalahaDisplay()
        self.players = players
        
        if len(players) != 2:
            raise ValueError("Exactly 2 players are required")
    
    def is_move_valid(self, player: int, pit: int) -> bool:
        """ Check if a move is valid. """
        return KalahaRules.is_move_valid(self.board, player, pit)
    
    def play_turn(self) -> bool:
        """ 
        Play a single turn for the current player. 
        Returns True if the game is over, False otherwise.
        """
        player = self.current_player
        player_obj = self.players[player]
        
        # get move from the current player
        pit = player_obj.get_move(self.board, player)
        
        # validate move
        while not self.is_move_valid(player, pit):
            print(f"Invalid move: {pit}")
            pit = player_obj.get_move(self.board, player)
        
        print(f"Player {player} chose pit {pit}")
        extra_turn = KalahaRules.make_move(self.board, player, pit)
        self.print_board()
        
        # check if game is over
        if self.is_game_over():
            self.finish_game()
            self.print_game_over()
            return True
        
        # switch player if no extra turn
        if not extra_turn:
            self.current_player = 1 - self.current_player
        else:
            print(f"Player {player} gets another turn!")
        
        return False
    
    def play_game(self) -> None:
        """ Play a full game of Kalaha. """
        print("Welcome to Kalaha!")
        self.print_board()
        
        game_over = False
        while not game_over:
            print("-" * 50)
            try:
                game_over = self.play_turn()
            except KeyboardInterrupt:
                print("\nGame aborted.")
                return
    
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