from board import KalahaBoard
from rules import KalahaRules
from player import Player
from agents.mcts_node import MCTSNode
import copy
import random
import math

class MCTSPlayer(Player):
    """
    Monte Carlo Tree Search player implementation.
    """
    def __init__(self, iterations: int = 100, exploration_weight: float = None, visualize_stats: bool = False):
        """
        Initialize the MCTS player.
        """
        self.iterations = iterations
        self.visualize_stats = visualize_stats

        if exploration_weight:
            self.exploration_weight = exploration_weight
        else:
            self.exploration_weight = math.sqrt(2)
    
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
                if result == -1:
                    # tie = don't update wins for anyone
                    new_result = 0
                    node.update(new_result)
                else:
                    node.update(result)
                    if node.parent:
                        # check for extra turn case
                        if node.player != node.parent.player:
                            result = 1 - result

                node = node.parent
        
        if self.visualize_stats:
            children = sorted(root.children, key=lambda c: c.visits, reverse=True)
            for c in children:
                print(f"move: {c.move}, visits: {c.visits}")

        # return the move with the highest visit count
        best_child = max(root.children, key=lambda c: c.visits)

        return best_child.move
    
    def __str__(self) -> str:
        return f"MCTS Player (iterations={self.iterations})"