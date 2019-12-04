from __future__ import annotations
from typing import Optional, List
from actor import *
import pygame
import random
from victoryScreen import victoryScreen

def load_map(filename: str) -> List[List[str]]:
    """
    Load the map data from the given filename and return as a list of lists.
    """

    with open(filename) as f:
        map_data = [line.split() for line in f]
    return map_data

class Game:
    """
    This class represents the main game.

    ==== Public Attributes: ====
    screen:
        initializes game screen
    stage_width:
        represents game stage width
    stage_height:
        represents game stage height
    size:
        represents icon size
    player:
        represents the player
    goal_stars:
        represents the goal_stars
    keys_pressed:
        represents the keys pressed in pygame module
    goal_message:
        represents the message of the goal for each level
    monster_count:
        represents the total number of squishy monsters in level one.
    setup_current_level:
        represents the method to setup the surrent level of the game
    pellet_count:
        represents the maximum number of pellets that can exist on
        the gameboard

    ==== Private Attributes: ====
    _running:
        represents if game is running or not
    _actors:
        list of actor objects
    _level:
        reperesents the current level of the game
    _max_level:
        represents the max level of the game

    """
    #  (Task 0) Complete the class documentation for this class by adding
    # attribute descriptions and types (make sure to separate public and
    # private attributes appropriately)

    def __init__(self) -> None:
        """
        Initialize a game that has a display screen and game actors.
        """

        self._running = False
        self.screen = None
        self.player = None
        self.keys_pressed = None

        # Attributes that get set during level setup
        self._actors = None
        self.stage_width, self.stage_height = 0, 0
        self.size = None
        self.goal_message = None

        # Attributes that are specific to certain levels
        self.goal_stars = 0  # Level 0
        self.monster_count = 0  # Level 1
        self.pellet_count = None
        # Method that takes care of level setup

    def set_player(self, player: Player) -> None:
        """
        Set the game's player to be the given <player> object.
        """

        self.player = player

    def add_actor(self, actor: Actor) -> None:
        """
        Add the given <actor> to the game's list of actors.
        """

        self._actors.append(actor)

    def remove_actor(self, actor: Actor) -> None:
        """
        Remove the given <actor> from the game's list of actors.
        """

        self._actors.remove(actor)

    def get_actor(self, x: int, y: int) -> Optional[Actor]:
        """
        Return the actor object that exists in the location given by
        <x> and <y>. If no actor exists in that location, return None.
        """

        for i in self._actors:
            if i.x == x and i.y == y:
                return i
        return None

    def on_init(self) -> None:
        """
        Initialize the game's screen, and begin running the game.
        """

        pygame.init()
        data = load_map("Maze-Man gameboard representation.txt")
        self.setup_ghost_game(data)
        self.screen = pygame.display.set_mode \
            (self.size, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self._running = True

    def on_event(self, event: pygame.Event) -> None:
        """
        React to the given <event> as appropriate.
        """

        if event.type == pygame.QUIT:
            self._running = False
        elif event.type == pygame.KEYDOWN:
            self.player.register_event(event.key)

    def game_won(self) -> bool:
        """
        Return True iff the game has been won, according to the current level.
        """

        #(Task 0) Move over your code from A0 here; adjust as needed
        obj = self.get_actor(self.player.x, self.player.y)

        if self.player.get_pellet_count() == self.pellet_count:
            return True
        else:
            return False

    def on_loop(self) -> None:
        """
        Move all actors in the game as appropriate.
        Check for win/lose conditions and stop the game if necessary.
        """

        self.keys_pressed = pygame.key.get_pressed()
        for actor in self._actors:
            actor.move(self)
        if self.player is None:
            print("You lose! :( Better luck next time.")
            self._running = False

        elif self.game_won():
            print("Congratulations, you won!")
            playagain = victoryScreen.victory_screen()
            self._running = False
            if playagain:
                self.__init__()
                self.on_execute()

    def on_render(self) -> None:
        """
        Render all the game's elements onto the screen.
        """

        self.screen.fill((0, 0, 0))
        for a in self._actors:
            rect = pygame.Rect(a.x * 24, a.y * 24, 24,
                               24)
            self.screen.blit(a.icon, rect)

        font = pygame.font.Font('freesansbold.ttf', 12)
        text = font.render(self.goal_message, True, (255, 255, 255), (0, 0, 0))
        textRect = text.get_rect()
        textRect.center = (self.stage_width * 24 // 2,
                           (self.stage_height + 0.5) * 24)
        self.screen.blit(text, textRect)

        pygame.display.flip()

    def on_cleanup(self) -> None:
        """
        Clean up and close the game.
        """

        pygame.quit()

    def on_execute(self) -> None:
        """
        Run the game until the game ends.
        """

        self.on_init()

        while self._running:
            pygame.time.wait(100)
            for event in pygame.event.get():
                self.on_event(event)
            self.on_loop()
            self.on_render()

        self.on_cleanup()

    def game_over(self) -> None:
        """
        Set the game as over (remove the player from the game).
        """

        self.player = None

    def setup_ghost_game(self, data) -> None:
        """
        Set up a game with a ghost that chases the player, and stars to collect.
        """

        w = len(data[0])
        h = len(
            data) + 1  # We add a bit of space for the text at the bottom

        self._actors = []
        self.stage_width, self.stage_height = w, h-1
        self.size = (w * 24, h * 24)
        self.pellet_count = 0

        player, chaser = None, None

        for i in range(len(data)):
            for j in range(len(data[i])):
                key = data[i][j]
                if key == 'P':
                    player = Player("MazeMan.png", j, i)
                elif key == 'G':
                    chaser = Ghost("Ghost.png", j, i, 0, 0)
                elif key == 'X':
                    self.add_actor(Wall("Ghost.png", j, i))
                elif key == 'O':
                    self.add_actor(Pellet("Pellet.png", j, i))
                    self.pellet_count += 1

        self.set_player(player)
        self.add_actor(player)
        self.add_actor(chaser)
        # Set the number of stars the player must collect to win
        self.goal_message = "Objective: Collect all of the pellets before the " \
                            "ghosts get you. You have 3 lives!"



