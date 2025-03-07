"""
Rules module for Kalaha game.
"""

from board import KalahaBoard

class KalahaRules:
    """
    Rules implementation for Kalaha game.
    """
    @staticmethod
    def is_move_valid(board: KalahaBoard, player: int, pit: int) -> bool:
        """ 
        Check if a move is valid. 
        Check if:
        - it's the player's pit
        - has stones
        """
        player_pits = board.get_player_pits(player)
        return pit in player_pits and board.get_stones(pit) > 0
    
    @staticmethod
    def make_move(board: KalahaBoard, player: int, pit: int) -> bool:
        """
        Make a move in the game. 
        Returns: True if the same player can make another move, False otherwise.
        """
        if not KalahaRules.is_move_valid(board, player, pit):
            raise ValueError(f"Invalid move: Pit {pit} is not a valid move for player {player}")
        
        # pick up stones from position pit
        stones = board.get_stones(pit)
        board.set_stones(pit, 0)
        
        # distribute stones
        current_pit = pit
        opponent_store = board.get_store(1 - player)
        
        # PART 1: iteration - distribute stones
        while stones > 0:
            # Move to next pit, use modulo to handle wrapping around
            current_pit = (current_pit + 1) % board.total_pits
            
            # skip opponent's store
            if current_pit == opponent_store:
                current_pit = (current_pit + 1) % board.total_pits
                
            # add a stone to the current pit
            board.add_stones(current_pit, 1)
            stones -= 1
        
        # PART 2: Special Rules
        # r1: last stone lands in the player's store - player gets another turn
        if current_pit == board.get_store(player):
            return True
            
        # r2: last stone lands in an empty pit on the player's side
        player_pits = board.get_player_pits(player)
        if current_pit in player_pits and board.get_stones(current_pit) == 1:
            # capture stones from the opposite pit
            opposite_pit = board.get_opposite_pit(current_pit)
            if board.get_stones(opposite_pit) > 0:  # only capture if there are stones
                # add captured stones and the capturing stone to the player's store
                total_capture = board.get_stones(opposite_pit) + 1
                board.add_stones(board.get_store(player), total_capture)
                # clear the pits
                board.set_stones(current_pit, 0)
                board.set_stones(opposite_pit, 0)
                
        return False
    
    @staticmethod
    def is_game_over(board: KalahaBoard) -> bool:
        """ Check if the game is over. Game is over when all pits are empty. """
        player0_empty = all(board.get_stones(pit) == 0 for pit in board.get_player_pits(0))
        player1_empty = all(board.get_stones(pit) == 0 for pit in board.get_player_pits(1))
        
        return player0_empty or player1_empty
    
    @staticmethod
    def finish_game(board: KalahaBoard) -> None:
        """ Finalize the game by moving remaining stones to respective stores. """
        for player in [0, 1]:
            for pit in board.get_player_pits(player):
                board.add_stones(board.get_store(player), board.get_stones(pit))
                board.set_stones(pit, 0)
    
    @staticmethod
    def get_winner(board: KalahaBoard) -> int:
        """ Get the winner of the game. """
        score0 = board.get_stones(board.get_store(0))
        score1 = board.get_stones(board.get_store(1))
        
        if score0 > score1:
            return 0
        elif score1 > score0:
            return 1
        else:
            return -1  # Tie