"""
Main module for Kalaha game.
"""

from game import KalahaGame
from player import HumanPlayer
from agents.mcts_player import MCTSPlayer
import math

def select_game_mode() -> int:
    """
    Allow user to select a game mode.
    Returns the selected mode number.
    """
    # print("Select game mode:")
    # print("1. Human vs Human")
    # print("2. Human vs AI (MCTS)")
    # print("3. AI vs Human (MCTS)")
    # print("4. AI vs AI (MCTS)")

    mode = 4

    return mode
    
    # while True:
    #     try:
    #         mode = int(input("Enter mode (1-4): "))
    #         if 1 <= mode <= 4:
    #             return mode
    #         print("Please enter a number between 1 and 4.")
    #     except ValueError:
    #         print("Please enter a valid number.")

def select_ai_difficulty() -> int:
    """
    Allow user to select AI difficulty.
    Returns number of MCTS iterations.
    """
    print("Select AI difficulty:")
    print("1. Easy (1000 iterations)")
    print("2. Medium (10000 iterations)")
    print("3. Hard (100000 iterations)")
    
    while True:
        try:
            difficulty = int(input("Enter difficulty (1-3): "))
            if difficulty == 1:
                return 1000
            elif difficulty == 2:
                return 10000
            elif difficulty == 3:
                return 100000
            print("Please enter a number between 1 and 3.")
        except ValueError:
            print("Please enter a valid number.")

def select_exploration_weight() -> float:
    """
    Allow user to select exploration weight.
    Returns float.
    """

    try:
        difficulty = float(input("Enter an exploration weight (float): "))
        if difficulty > 0:
            return difficulty
        print("Please enter a positive float.")
    except ValueError:
        print("Please enter a valid number.")

def configure_game(mode: int) -> KalahaGame:
    """
    Configure the game based on the selected mode.
    Returns a configured KalahaGame instance.
    """
    if mode == 1:  # Human vs Human
        players = [HumanPlayer(), HumanPlayer()]
        return KalahaGame(players)
    
    elif mode == 2:  # Human vs AI
        iterations = select_ai_difficulty()
        players = [HumanPlayer(), MCTSPlayer(iterations)]
        return KalahaGame(players)
    
    elif mode == 3:  # AI vs Human
        iterations = select_ai_difficulty()
        players = [MCTSPlayer(iterations), HumanPlayer()]
        return KalahaGame(players)

    elif mode == 4:  # AI vs AI
        iterations = 10000
        iterations2 = 100
        exp_weight = math.sqrt(2)
        exp_weight_2 = math.sqrt(2)
        players = [MCTSPlayer(iterations, exploration_weight=exp_weight), MCTSPlayer(iterations2, exploration_weight=exp_weight_2)]
        return KalahaGame(players)

def one_game():
    """
    Main function to run the Kalaha game.
    """
    print("Welcome to Kalaha Game!")
    print("-" * 50)
    
    # select game mode: Human vs Human, Human vs AI, or AI vs Human
    mode = select_game_mode()
    
    # configure and start the game
    game = configure_game(mode)
    
    # play the game
    try:
        game.play_game()
        return game
    except KeyboardInterrupt:
        print("\nGame aborted. Goodbye!")

def main():
    results = []
    for i in range(10):
        game = one_game()
        player_win = game.get_winner()
        
        # score = game.board.get_score()
        results.append((player_win))
    print(results)

if __name__ == "__main__":
    main()