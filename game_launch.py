"""
game_launch.py: Launches the Blackjack game.

This module includes the following:
- Main script for launching the Blackjack game.
"""

from game import Game

if __name__ == '__main__':
    """
    Main script for launching the Blackjack game.

    Creates an instance of the Game class and starts the Blackjack game.
    """
    current_game = Game()
    current_game.start_game()

# TODO:  додати можливість залишатись в кімнаті чи іти в іншу
# TODO: докстрінги до кожного класу, функції та рідмі
