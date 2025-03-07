"""
Display module for Kalaha game.
"""

from board import KalahaBoard

class KalahaDisplay:
    """
    Display handling for Kalaha game.
    """
    @staticmethod
    def print_board(board: KalahaBoard) -> None:
        """ Print the current board state. """
        # print player 1's pits (reversed)
        p1_pits = board.get_player_pits(1)
        p1_pits.reverse()  # in order to display in opposite direction
        
        print("\nPlayer 1 (top):")
        print("  ", end="")
        for pit in p1_pits:
            print(f"{board.get_stones(pit):2d} ", end="")
        print()
        
        # print stores
        print(f"{board.get_stones(board.get_store(1)):2d}", end="")
        print(" " * (board.pits_per_player * 3), end="")
        print(f"{board.get_stones(board.get_store(0)):2d}")
        
        # print player 0's pits
        print("  ", end="")
        for pit in board.get_player_pits(0):
            print(f"{board.get_stones(pit):2d} ", end="")
        print()
        print("Player 0 (bottom)")
        
        # print pit indices for reference
        print("\nPit indices:")
        print("  ", end="")
        for pit in p1_pits:
            print(f"{pit:2d} ", end="")
        print()
        
        print("  ", end="")
        for pit in board.get_player_pits(0):
            print(f"{pit:2d} ", end="")
        print("\n")
    
    @staticmethod
    def print_game_over(board: KalahaBoard, winner: int) -> None:
        """ Print game over message with final scores. """
        if winner == -1:
            print("Game over! It's a tie!")
        else:
            print(f"Game over! Player {winner} wins!")
        
        print(f"Final score - Player 0: {board.get_stones(board.get_store(0))}, " + 
              f"Player 1: {board.get_stones(board.get_store(1))}")

