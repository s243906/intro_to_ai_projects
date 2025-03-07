"""
Game simulation for Kahala.
"""

from typing import Tuple, List

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
        self.pits_per_player = pits_per_player
        self.total_pits = pits_per_player * 2 + 2  # with stores
        self.player_stores = [pits_per_player, pits_per_player * 2 + 1]  # indices for players 0 and 1
        self.board, self.current_player = self._init_game(stones_per_pit)
        
    def _init_game(self, stones_per_pit: int) -> Tuple[List[int], int]:
        """ Initialize the game board and starting player. """
        board = []

        # iterate through the pits, put 4 stones (unless it's a store)
        for i in range(self.total_pits):
            if i in self.player_stores:  
                board.append(0)
            else:
                board.append(stones_per_pit)
                
        return board, 0  # Player 0 starts
    
    def _get_player_pits(self, player: int) -> List[int]:
        """ Get the indices of pits owned by a player (excluding store). """
        if player == 0:
            return list(range(0, self.pits_per_player))
        else:
            return list(range(self.pits_per_player + 1, self.player_stores[1]))
    
    def is_move_valid(self, player: int, pit: int) -> bool:
        """ 
            Check if a move is valid. 
            Check if:
            - it's the player's pit
            - has stones
        """
        player_pits = self._get_player_pits(player)
        return pit in player_pits and self.board[pit] > 0
    
    def move(self, player: int, pit: int) -> bool:
        """
            Make a move in the game. 
            Returns: True if the same player can make another move, False otherwise.
        """
        if not self.is_move_valid(player, pit):
            raise ValueError(f"Invalid move: Pit {pit} is not a valid move for player {player}")
        
        # pick up stones from position pit
        stones = self.board[pit]
        self.board[pit] = 0
        
        # distribute stones
        current_pit = pit
        opponent_store = self.player_stores[1 - player]
        
        # PART 1: iteration
        while stones > 0:

            # why modulo? just to make sure that we don't get index out of range: ask hubert
            current_pit = (current_pit + 1) % self.total_pits
            
            # skip opponent's store
            if current_pit == opponent_store:
                current_pit = (current_pit + 1) % self.total_pits
                
            # add a stone to the current pit
            self.board[current_pit] += 1
            stones -= 1
        
        
        # PART 2: Special Rules

        # r1: last stone lands in the player's store - player gets another turn
        if current_pit == self.player_stores[player]:
            return True
            
        # r2: last stone lands in an empty pit on the player's side
        player_pits = self._get_player_pits(player)
        if current_pit in player_pits and self.board[current_pit] == 1:
            # capture stones from the opposite pit
            opposite_pit = self.total_pits - 2 - current_pit
            if self.board[opposite_pit] > 0:  # only capture if there are stones
                # add captured stones and the capturing stone to the player's store
                self.board[self.player_stores[player]] += self.board[opposite_pit] + 1
                # clear the pits
                self.board[current_pit] = 0
                self.board[opposite_pit] = 0
                
        return False
    
    def is_game_over(self) -> bool:
        """ Check if the game is over. Game is over when all pits are empty. """
        player0_empty = all(self.board[pit] == 0 for pit in self._get_player_pits(0))
        player1_empty = all(self.board[pit] == 0 for pit in self._get_player_pits(1))
        
        return player0_empty or player1_empty
    
    def finish_game(self) -> None:
        """ Finalize the game by moving remaining stones to respective stores. """
        for player in [0, 1]:
            for pit in self._get_player_pits(player):
                self.board[self.player_stores[player]] += self.board[pit]
                self.board[pit] = 0
    
    def get_winner(self) -> int:
        """ Get the winner of the game. """
        if not self.is_game_over():
            self.finish_game()
            
        score0 = self.board[self.player_stores[0]]
        score1 = self.board[self.player_stores[1]]
        
        if score0 > score1:
            return 0
        elif score1 > score0:
            return 1
        else:
            return -1
    
    def print_board(self) -> None:
        """ Print the current board state. """
        # print player 1's pits (reversed)
        p1_pits = self._get_player_pits(1)
        p1_pits.reverse()  # in order to display in opposite direction
        
        print("\nPlayer 1 (top):")
        print("  ", end="")
        for pit in p1_pits:
            print(f"{self.board[pit]:2d} ", end="")
        print()
        
        # print stores
        print(f"{self.board[self.player_stores[1]]:2d}", end="")
        print(" " * (self.pits_per_player * 3), end="")
        print(f"{self.board[self.player_stores[0]]:2d}")
        
        # print player 0's pits
        print("  ", end="")
        for pit in self._get_player_pits(0):
            print(f"{self.board[pit]:2d} ", end="")
        print()
        print("Player 0 (bottom)")
        
        # print pit indices for reference
        print("\nPit indices:")
        print("  ", end="")
        for pit in p1_pits:
            print(f"{pit:2d} ", end="")
        print()
        
        print("  ", end="")
        for pit in self._get_player_pits(0):
            print(f"{pit:2d} ", end="")
        print("\n")


def play_game():
    """ Run a two-player game of Kalaha. """
    game = KalahaGame()
    player = 0
    
    print("Welcome to Kalaha!")
    game.print_board()
    
    while not game.is_game_over():
        try:
            print("-"*50)
            pit = int(input(f"Player {player}, choose a pit: "))
            
            if game.is_move_valid(player, pit):
                extra_turn = game.move(player, pit)
                game.print_board()
                
                if not extra_turn:
                    player = 1 - player  # switch player if no extra turn
                else:
                    print(f"Player {player} gets another turn!")
            else:
                print("Invalid move. Try again.")
        except ValueError as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nGame aborted.")
            return
    
    # game is over, determine the winner
    game.finish_game()
    winner = game.get_winner()
    
    if winner == -1:
        print("Game over! It's a tie!")
    else:
        print(f"Game over! Player {winner} wins!")
    
    print(f"Final score - Player 0: {game.board[game.player_stores[0]]}, Player 1: {game.board[game.player_stores[1]]}")


if __name__ == "__main__":
    play_game()