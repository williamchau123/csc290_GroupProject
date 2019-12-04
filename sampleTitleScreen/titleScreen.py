import pygame
# The title screen is composed of 3 sequences. Those are the intro, the menu,
# and the exit sequence. The current sequence is denoted by the current_stage
# variable


def title_screen():

    pygame.init()  # create the game window
    display_width = 800
    display_height = 600
    black = (0, 0, 0)
    yellow = (255, 255, 0)
    white = (255, 255, 255)
    current_stage = "intro sequence"

    game_title_font = 'sampleTitleScreen/8bit_wonder/8-BIT WONDER.ttf'
    size_change = 0.0075
    size_multiplier = 0.75

    maze_man_x = -30
    maze_man_y = 0
    ghost_x = maze_man_x-150
    ghost_y = 0
    maze_man_speed = 15
    maze_man_size = (100, 100)
    pellet_size = (25, 25)
    ghost_speed = 15
    ghost_size = (100, 100)

    pellet_img = pygame.image.load("sprites/Pellet.png")
    maze_man_img = pygame.image.load('sprites/MazeMan.png')
    ghost_img = pygame.image.load("sprites/Ghost.png")

    # Scales all the images to the appropriate size
    maze_man = pygame.transform.scale(maze_man_img, maze_man_size)
    pellet = pygame.transform.scale(pellet_img, pellet_size)
    ghost = pygame.transform.scale(ghost_img, ghost_size)

    game_display = pygame.display.set_mode((display_width, display_height))
    clock = pygame.time.Clock()     # need this to set the FPS count
    pygame.display.set_caption("Maze-Man")  # game window title
    stopped = False

    def draw_maze_man(x, y):
        """
        The substitutes pygame.transform.scale instance and the coordinates of
        the instance to game_display instance to draw the maze-man to the screen
        .
        """
        game_display.blit(maze_man, (x, y))

    def draw_ghost(x, y):
        """
        The substitutes pygame.transform.scale instance and the coordinates of
        the instance to game_display instance to draw the ghost to the screen.
        """
        game_display.blit(ghost, (x, y))

    def draw_pellets(man_x, man_y):
        """
        It draws the pellet that the maze-man is going to to eat.
        """
        pellet_x = 50
        pellet_y = 40
        while pellet_x < display_width or pellet_y < display_height:
            # check if the MazeMan has eaten the pellet
            if pellet_y > (man_y+40) or (pellet_x > (man_x+5)
                                         and pellet_y == (man_y+40)):
                game_display.blit(pellet, (pellet_x, pellet_y))
            if pellet_x >= display_width:  # end of row, reset X and go down
                pellet_x = 50
                pellet_y += 150
            else:  # Draw next pellet on the row
                pellet_x += 100

    def draw_title(title, font, color):
        """
        It draws the title with specified font and color in input.
        """
        title_font = pygame.font.Font(font, 60)
        text_surface = title_font.render(title, True, color)
        text_rect = text_surface.get_rect()

        text_rect.center = ((display_width/2), (display_height/2))  # centers
        game_display.blit(text_surface, text_rect)                  # the button

    def play_button(message, font, color, multiplier=1.0):
        """
        It return the click when the user clicked the title screen after the
        animation.
        """
        play_font = pygame.font.Font(font, int(20*multiplier))  # the multiplier
        text_surface = play_font.render(message, True, color)    # creates the
        text_rect = text_surface.get_rect()                      # animations

        text_rect.center = ((display_width/2), 3*(display_height/4))
        game_display.blit(text_surface, text_rect)

        has_clicked = check_mouse_click(text_rect.left, text_rect.w, text_rect.h
                                        , text_rect.top)
        return has_clicked

    def check_mouse_click(left_bound, width, height, top_bound):
        """
        When click is executed by play_button function, it check whether the
        click was executed in an appropriate position.
        """
        mouse = pygame.mouse.get_pos()
        clicks = pygame.mouse.get_pressed()
        mouse_x = mouse[0]
        mouse_y = mouse[1]

        if (left_bound < mouse_x < (left_bound+width)) and \
                (top_bound < mouse_y < (top_bound+height)):  # We're checking if
            if clicks[0] == 1:                            # if the mouse has
                return True                               # clicked within range
        return False                                      # of the play button

    pygame.time.wait(1000)  # wait some time before starting the game
    while not stopped:
        game_display.fill(black)

        for event in pygame.event.get():  # retrieve a list of events (clicks,.)
            if event.type == pygame.QUIT:
                stopped = True

        if current_stage == "intro sequence":
            if pygame.mouse.get_pressed()[0] == 1:
                current_stage = "menu"  # Update the intro and the menu
                maze_man_x = -150
            if ghost_x >= display_width:  # move ghost and mazeMan to next row
                maze_man_x = -30
                maze_man_y += 150
                ghost_x = maze_man_x-150
                ghost_y += 150
                if ghost_y >= display_height:  # all rows have been cleared
                    current_stage = "menu"
                    maze_man_y = (display_height/2) - 150  # Move the ghost off
                    ghost_y = (display_height/2) - 150     # screen and the
                    ghost_x = -150                         # mazeMan into place
                    pygame.time.wait(300)
                else:
                    pygame.time.wait(500)  # pause in between row changes
            else:  # Otherwise ghost and mazeMan keep moving
                maze_man_x += maze_man_speed
                ghost_x += ghost_speed

            draw_pellets(maze_man_x, maze_man_y)

        elif current_stage == "menu":
            maze_man_y = display_height/2 - 150
            # setting the mazeman and the ghost to the correct Y position
            ghost_y = display_height/2 - 150
            ghost_x = -150  # setting ghost to be out of the menu
        #                 #Update the intro and the menu
            if maze_man_x <= (display_width/2 - 50):  # mazeMan enters
                maze_man_x += maze_man_speed  # from the left side
            if size_multiplier > 0.9 or size_multiplier < 0.75:  # for vibrating
                size_change *= -1                                # play button
            size_multiplier += size_change

            draw_title("MazeMan", game_title_font, yellow)
            clicked = play_button("Play", game_title_font, white
                                  , size_multiplier)
            if clicked:
                current_stage = "exit sequence"

        elif current_stage == "exit sequence":
            if ghost_x <= display_width:    # In this sequence, the ghost chases
                if ghost_x >= (maze_man_x - 150):  # the mazeMan. But we don't
                    maze_man_x += maze_man_speed  # want him to move until the
                ghost_x += ghost_speed            # ghost is close enough
            else:
                pygame.time.wait(250)
                stopped = True

        draw_maze_man(maze_man_x, maze_man_y)
        draw_ghost(ghost_x, ghost_y)
        pygame.display.update()
        clock.tick(30)  # frames per second
