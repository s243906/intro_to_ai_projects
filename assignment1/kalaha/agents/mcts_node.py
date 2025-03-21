"""
Monte Carlo Tree Search module for Kalaha game.
"""
import math
import random
import copy
from typing import List, Dict, Tuple, Optional
from board import KalahaBoard
from rules import KalahaRules

class MCTSNode:
    """
    Represents a node in the Monte Carlo Tree Search.
    The node contains information about the current game state, player, and move that led to this node.
    """
    def __init__(self, board: KalahaBoard, player: int, parent=None, move=None):
        """Initialize a new MCTS node."""
        self.board = board
        self.player = player
        self.parent = parent
        self.move = move
        self.children: List['MCTSNode'] = []
        self.wins = 0
        self.visits = 0
        self.untried_moves = self._get_untried_moves()
    
    def _get_untried_moves(self) -> List[int]:
        """
            Get list of valid moves that haven't been tried yet.
            The valid moves are the pits with stones for the current player.
        """
        return [pit for pit in self.board.get_player_pits(self.player)
                if self.board.get_stones(pit) > 0]
    
    def add_child(self, move: int) -> 'MCTSNode':
        """ Add a child node with the specified move. """
        # copy of the board - we do not want to modify the original board
        new_board = copy.deepcopy(self.board)
        
        # make the move
        # note: make_move returns True if the player gets an extra turn
        extra_turn = KalahaRules.make_move(new_board, self.player, move)
        # determine the next player
        next_player = self.player if extra_turn else 1 - self.player
        
        # create a new node
        child = MCTSNode(new_board, next_player, parent=self, move=move)

        self.untried_moves.remove(move)
        self.children.append(child)

        return child
    
    def update(self, result: float) -> None:
        """ Update node statistics. """
        self.visits += 1
        # print(f"result: {result}")
        self.wins += result
    
    def uct_select_child(self, is_even: bool, exploration_weight: float = 1.0) -> 'MCTSNode':
        """ Select child node with highest UCT value. """
        log_visits = math.log(self.visits)
        
        def uct(child):
            # exploitation term
            win_rate = child.wins / child.visits if child.visits > 0 else 0
            # exploration term
            exploration = math.sqrt(log_visits / child.visits) if child.visits > 0 else float('inf')
            return win_rate + exploration_weight * exploration
        
        if is_even:
            return max(self.children, key=uct)
        
        return min(self.children, key=uct)
    
    def is_terminal(self) -> bool:
        """ Check if the node represents a terminal state. """
        return KalahaRules.is_game_over(self.board)
    
    def rollout(self) -> float:
        """ Simulate a random game from this node until terminal state. """
        # copy of the board - we do not want to modify the original board
        sim_board = copy.deepcopy(self.board)
        sim_player = self.player
        
        # simulate until game over
        while not KalahaRules.is_game_over(sim_board):
            # get valid moves
            valid_moves = [pit for pit in sim_board.get_player_pits(sim_player) 
                          if sim_board.get_stones(pit) > 0]
            
            if not valid_moves:
                break
            
            # choose a random move
            move = random.choice(valid_moves)
            # make the move
            extra_turn = KalahaRules.make_move(sim_board, sim_player, move)
            # switch player if no extra turn
            if not extra_turn:
                sim_player = 1 - sim_player
        
        # finalize the game
        KalahaRules.finish_game(sim_board)
        
        # determine the result
        winner = KalahaRules.get_winner(sim_board)
        
        # return the result relative to the original player
        if winner == -1:  # tie case
            return 0.0
        elif winner == self.parent.player:  # win for the original player
            return 1.0
        else:  # loss for the original player
            return 0.0

    def __str__(self) -> str:
        return f"MCTSNode(player={self.player}, move={self.move}, wins={self.wins}, visits={self.visits})"