import pygame


def victory_screen():

    pygame.init()  # create the game window
    display_width = 800
    display_height = 600
    black = (0, 0, 0)
    yellow = (255, 255, 0)
    white = (255, 255, 255)
    current_stage = "intro sequence 1"

    game_font = 'victoryScreen/8bit_wonder/8-BIT WONDER.ttf'
    size_change = 0.0025
    size_multiplier = 0.7
    light_length = 150  # see drawTheLight() for its use

    maze_manX = -200
    maze_manY = display_height/2
    ghostX = maze_manX-150
    ghostY = display_height/2
    maze_man_speed = 10
    maze_man_size = (100, 100)
    ghost_speed = 10
    ghost_size = (100, 100)

    maze_man_img = pygame.image.load('MazeMan.png')
    ghost_img = pygame.image.load("Ghost.png")

    # Scales all the images to the appropriate size
    maze_man = pygame.transform.scale(maze_man_img, maze_man_size)
    ghost = pygame.transform.scale(ghost_img, ghost_size)

    gameDisplay = pygame.display.set_mode((display_width, display_height))
    clock = pygame.time.Clock()     # need this to set the FPS count
    pygame.display.set_caption("Maze-Man")  # game window title
    stopped = False

    def drawMazeMan(x, y):
        gameDisplay.blit(maze_man, (x, y))

    def drawGhost(x, y):
        gameDisplay.blit(ghost, (x, y))

    def checkMouseClick(leftBound, width, height, topBound):
        mouse = pygame.mouse.get_pos()
        clicks = pygame.mouse.get_pressed()
        mouseX = mouse[0]
        mouseY = mouse[1]

        if (leftBound < mouseX < (leftBound+width)) and \
                (topBound < mouseY < (topBound+height)):  # We're checking if
            if clicks[0] == 1:                            # if the mouse has
                return True                               # clicked within range
        return False                                      # of the play button

    def drawButton(message, font, color, size, xy_position, multiplier=1.0):

        # a small clarification here is that xy_position is a tuple of two
        # integers each between 0 and 1 representing the far left and far right
        # of the display for x and the top and bottom of the display for y
        # respectively

        playFont = pygame.font.Font(font,
                                    int(size * multiplier))  # the multiplier
        textSurface = playFont.render(message, True, color)  # creates the
        textRect = textSurface.get_rect()  # animations

        textRect.center = (
        (display_width * xy_position[0]), display_height*xy_position[1])
        gameDisplay.blit(textSurface, textRect)

        clicked = checkMouseClick(textRect.left, textRect.w, textRect.h,
                                  textRect.top)
        return clicked

    def drawText(text, font, color, size, xy_position=(0.5, 0.5)):
        textFont = pygame.font.Font(font, size)
        textSurface = textFont.render(text, True, color)
        textRect = textSurface.get_rect()

        textRect.center = ((display_width*xy_position[0]),
                           (display_height*xy_position[1]))
        gameDisplay.blit(textSurface, textRect)

    # Represents the white to black gradient at the edge of the screen
    # How it works? Draws consecutive rectangles of display_height height and 1
    # pixel width of gradually darkening color (from white to black)

    def drawTheLight(x_end_position, length):
        # length: The gradient's length in pixels
        # x_end_position: the x coordinate where the gradient ends; also keeps
        # track of the position of each rectangle
        white_to_black = max(min(length, 255), 0)
        color = (white_to_black, white_to_black, white_to_black)
        line_thickness = 1
        while white_to_black > 0:
            pygame.draw.rect(gameDisplay, color, (x_end_position -
                                                  line_thickness, 0
                                                               , line_thickness
                                                               , display_height)
                                          )
            # pygame rect (x, y, width, height)
            x_end_position -= 1
            white_to_black -= 1
            color = (white_to_black, white_to_black, white_to_black)

    def pre_intro_sequence():
        # Why is this function important? If the mazeMan exits the stage
        # through the left side of the maze, then entering the victory screen
        # from the left side is unnatural and breaks the chain of events.

        # Part 1
        pygame.time.wait(1000)
        drawText("A few moments later", game_font, white, 20)
        pygame.display.update()
        pygame.time.wait(2500)

        # Part 2
        gameDisplay.fill(black)
        drawTheLight(display_width, light_length)
        pygame.display.update()
        pygame.time.wait(2000)

    pre_intro_sequence()
    while not stopped:
        gameDisplay.fill(black)

        for event in pygame.event.get():  # retrieve a list of events (clicks,.)
            if event.type == pygame.QUIT:
                stopped = True

        if current_stage == "intro sequence 1":
            if ghostX > display_width/2:
                pygame.time.wait(1000)
                current_stage = "intro sequence 2"

            if maze_manX > display_width/2:
                ghostX += ghost_speed

            if light_length > 0:  # the gradient slowly shrinks
                light_length -= 1

            maze_manX += maze_man_speed


            drawTheLight(display_width, light_length)

        if current_stage == "intro sequence 2":  # intermediate sequence where
            if ghostX < -150:                    # the ghost moves off screen
                current_stage = "interactive sequence"
                maze_manX = -200
                maze_manY = display_height / 2 - 150
                ghostX = display_width + 150
                ghostY = display_height / 2 - 150
                pygame.time.wait(250)
            ghostX -= ghost_speed

        if current_stage == "interactive sequence":
            if maze_manX < display_width/2 - 50:  # bring mazeMan to center
                maze_manX += maze_man_speed       # screen

            size_multiplier += size_change
            if size_multiplier > 0.9 or size_multiplier < 0.7:  # for vibrating
                size_change *= -1                                # play button

            drawText("Victory", game_font, yellow, 60)
            clicked_play = drawButton("Play Again", game_font, white, 20,
                                      (0.25, 0.75), size_multiplier)
            clicked_exit = drawButton("Quit", game_font, white, 20,
                                      (0.75, 0.75), size_multiplier)
            if clicked_play or clicked_exit:
                current_stage = "exit sequence"

        if current_stage == "exit sequence":
            if maze_manX > display_width:
                if clicked_exit:
                    return False
                else:
                    return True
            maze_manX += maze_man_speed


        drawMazeMan(maze_manX, maze_manY)
        drawGhost(ghostX, ghostY)
        pygame.display.update()
        clock.tick(30)

