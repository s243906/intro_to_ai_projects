"""
Main module for Kalaha game.
"""

from game import KalahaGame
from player import HumanPlayer
from agents.mcts_player import MCTSPlayer

def select_game_mode() -> int:
    """
    Allow user to select a game mode.
    Returns the selected mode number.
    """
    print("Select game mode:")
    print("1. Human vs Human")
    print("2. Human vs AI (MCTS)")
    print("3. AI vs Human (MCTS)")
    
    while True:
        try:
            mode = int(input("Enter mode (1-3): "))
            if 1 <= mode <= 3:
                return mode
            print("Please enter a number between 1 and 3.")
        except ValueError:
            print("Please enter a valid number.")

def select_ai_difficulty() -> int:
    """
    Allow user to select AI difficulty.
    Returns number of MCTS iterations.
    """
    print("Select AI difficulty:")
    print("1. Easy (200 iterations)")
    print("2. Medium (1000 iterations)")
    print("3. Hard (10000 iterations)")
    
    while True:
        try:
            difficulty = int(input("Enter difficulty (1-3): "))
            if difficulty == 1:
                return 200
            elif difficulty == 2:
                return 1000
            elif difficulty == 3:
                return 10000
            print("Please enter a number between 1 and 3.")
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
        visualize_stats = False
        players = [HumanPlayer(), MCTSPlayer(iterations, visualize_stats=visualize_stats)]
        return KalahaGame(players)
    
    elif mode == 3:  # AI vs Human
        iterations = select_ai_difficulty()
        visualize_stats = False
        players = [MCTSPlayer(iterations, visualize_stats=visualize_stats), HumanPlayer()]
        return KalahaGame(players)

def main():
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
    except KeyboardInterrupt:
        print("\nGame aborted. Goodbye!")

if __name__ == "__main__":
    main()