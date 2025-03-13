from board import KalahaBoard
from rules import KalahaRules
from player import Player
from agents.mcts_node import MCTSNode
import copy
import random

class MCTSPlayer(Player):
    """
    Monte Carlo Tree Search player implementation.
    """
    def __init__(self, iterations: int = 1000, exploration_weight: float = 1.0, log: bool = True):
        """
        Initialize the MCTS player.
        
        Parameters:
        iterations (int): Number of MCTS iterations to perform.
        exploration_weight (float): Weight of exploration term in UCT formula.
        """
        self.iterations = iterations
        self.exploration_weight = exploration_weight
        self.log = log
    
    def get_move(self, board: KalahaBoard, player_id: int) -> int:
        """
        Determine the best move using MCTS.
        """
        # create root node
        root = MCTSNode(copy.deepcopy(board), player_id)
        
        # check if there are valid moves
        if not root.untried_moves:
            return -1
        
        # run MCTS for the specified number of iterations
        for _ in range(self.iterations):
            # 1. selection phase: select a node to expand
            node = root

            # while node is fully expanded and not terminal
            while node.untried_moves == [] and node.children:
                node = node.uct_select_child(self.exploration_weight)

            # 2. expansion phase: Add a child node if possible)
            if node.untried_moves:
                move = random.choice(node.untried_moves)
                node = node.add_child(move)
            
            # simulation phase: Perform a random rollout
            result = node.rollout()
            
            # backpropagation phase: Update statistics
            while node:
                node.update(result)
                node = node.parent
        
        # return the move with the highest visit count
        best_child = max(root.children, key=lambda c: c.visits)

        return best_child.move
    
    def __str__(self) -> str:
        return f"MCTS Player (iterations={self.iterations})"