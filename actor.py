from __future__ import annotations
import pygame
from typing import Optional


class Actor:
    """
    A class to represent all the game's actors. This class includes any
    attributes/methods that every actor in the game must have.

    This is an abstract class. Only subclasses should be instantiated.

    === Public Attributes ===
    x:
        x coordinate of this actor's location on the stage
    y:
        y coordinate of this actor's location on the stage
    icon:
        the image representing this actor
    """
    x: int
    y: int
    icon: pygame.Surface

    def __init__(self, icon_file, x, y):
        """Initialize an actor with the given image <icon_file> and the
        given <x> and <y> position on the game's stage.
        """

        self.x, self.y = x, y
        self.icon = pygame.image.load(icon_file)

    def move(self, game: 'Game') -> None:
        """Move this actor by taking one step of its animation."""

        raise NotImplementedError

class Player(Actor):
    """
    A class to represent a Player in the game.
    """
    # === Private Attributes ===
    # _stars_collected:
    #       the number of stars the player has collected so far
    # _last_event:
    #       keep track of the last key the user pushed down
    # _smooth_move:
    #       represent on/off status for smooth player movement

    x: int
    y: int
    icon: pygame.Surface
    _pellet_collected: int
    _last_event: Optional[int]
    _smooth_move: bool
    _keys_collected: int

    def __init__(self, icon_file: str, x: int, y: int) -> None:
        """Initalize a Player with the given image <icon_file> at the position
        <x> and <y> on the stage."""

        super().__init__(icon_file, x, y)
        self._pellet_collected = 0
        self._last_event = None # This is used for precise movement
        self._keys_collected = 0

    def get_pellet_count(self) -> int:
        """
        Return the number of stars collected.
        """

        return self._pellet_collected

    def register_event(self, event: int) -> None:
        """
        Keep track of the last key <event> the user made.
        """

        self._last_event = event

    def get_key_count(self) -> int:
        """
        Return the number of keys collected
        """
        return self._keys_collected

    def move(self, game: 'Game') -> None:
        """
        Move the player on the <game>'s stage based on keypresses.
        """

        if self._last_event:
            dx, dy = 0, 0

            if not type(game.get_actor(self.x - 1, self.y)) == Wall:
                if game.keys_pressed[pygame.K_LEFT]:
                    dx -= 1
            if not type(game.get_actor(self.x + 1, self.y)) == Wall:
                    dx += 1
            if not type(game.get_actor(self.x, self.y - 1)) == Wall:
                if game.keys_pressed[pygame.K_UP]:
                    dy -= 1
            if not type(game.get_actor(self.x, self.y + 1)) == Wall:
                if game.keys_pressed[pygame.K_DOWN]:
                    dy += 1

            if not type(game.get_actor(self.x - 1, self.y)) == Wall:
                if game.keys_pressed[pygame.K_a]:
                    dx -= 1
            if not type(game.get_actor(self.x + 1, self.y)) == Wall:
                if game.keys_pressed[pygame.K_d]:
                    dx += 1
            if not type(game.get_actor(self.x, self.y - 1)) == Wall:
                if game.keys_pressed[pygame.K_w]:
                    dy -= 1
            if not type(game.get_actor(self.x, self.y + 1)) == Wall:
                if game.keys_pressed[pygame.K_s]:
                    dy += 1

            new_x, new_y = self.x + dx, self.y + dy

            if type(game.get_actor(new_x, new_y)) == Pellet:
                self._pellet_collected += 1
                actor = game.get_actor(new_x, new_y)
                game.remove_actor(actor)

            new_x, new_y = self.x + dx, self.y + dy

            # (Task 0) Move over your code from A0 here; adjust
            # i.e. Check if move is possible / if star is to be collected, etc.

            self.x, self.y = new_x, new_y

# === classes for immobile objects


class Pellet(Actor):
    """
    A class to represent a Star in the game.
    """
    x: int
    y: int
    icon: pygame.Surface

    def move(self, game: 'Game') -> None:
        """
        A Star cannot move, so do nothing.
        """

        pass


class Wall(Actor):
    """
    A class to represent a Wall in the game.
    """
    x: int
    y: int
    icon: pygame.Surface

    def move(self, game: 'Game') -> None:
        """
        A Wall cannot move, so do nothing.
        """

        pass

# === Ghost classes


class Ghost(Actor):
    """
    A class to represent monsters that kill the player upon contact.
    """
    # === Private attributes ===
    # _dx:
    #   the horizontal distance this monster will move during each step
    # _dy:
    #   the vertical distance this monster will move during each step
    # _delay:
    #   the speed the monster moves at
    # _delay_count:
    #   used to keep track of the monster's delay in speed
    x: int
    y: int
    icon: pygame.Surface
    _dx: float
    _dy: float
    _delay: int
    _delay_count: int

    def __init__(self, icon_file: str, x: int, y: int, dx: float, dy: float) -> None:
        """Initalize a monster with the given <icon_file> as its image,
        <x> and <y> as its position, and <dx> and <dy> being how much
        it moves by during each animation in the game. The monster also
        has a delay which could optionally be used to slow it down."""

        super().__init__(icon_file, x, y)
        self._dx = dx
        self._dy = dy
        self._delay = 5
        self._delay_count = 1

    def move(self, game: 'Game') -> None:
        """
         Move the ghost on the <game>'s screen based on the player's location.
         Check if the ghost has caught the player after each move.
        """

        if not game.player is None:
            if game.player.x > self.x:
                self.x += self._dx
            elif game.player.x < self.x:
                self.x -= self._dx
            elif game.player.y > self.y:
                self.y += self._dy
            elif game.player.y < self.y:
                self.y -= self._dy

            self.check_player_death(game)

    def check_player_death(self, game: 'Game') -> None:
        """Make the game over if this monster has hit the player."""

        if game.player is None:
            game.game_over()
        elif self.x == game.player.x and self.y == game.player.y:
            game.game_over()
