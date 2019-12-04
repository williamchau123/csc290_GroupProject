"""
This module initializes and runs the main game.
"""
from sampleTitleScreen import titleScreen

from game import Game

if __name__ == "__main__":

    titleScreen.title_screen()
    game = Game()
    game.on_execute()
