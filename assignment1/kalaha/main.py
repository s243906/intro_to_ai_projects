"""
Main module for Kalaha game.
"""

from game import KalahaGame

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
    game.print_game_over()


if __name__ == "__main__":
    play_game()