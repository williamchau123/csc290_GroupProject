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

    game_title_font = '8bit_wonder/8-BIT WONDER.ttf'
    size_change = 0.0075
    size_multiplier = 0.75

    maze_manX = -30
    maze_manY = 0
    ghostX = maze_manX-150
    ghostY = 0
    maze_man_speed = 15
    maze_man_size = (100, 100)
    pellet_size = (25, 25)
    ghost_speed = 15
    ghost_size = (100, 100)

    pellet_img = pygame.image.load("Pellet.png")
    maze_man_img = pygame.image.load('MazeMan.png')
    ghost_img = pygame.image.load("Ghost.png")

    # Scales all the images to the appropriate size
    maze_man = pygame.transform.scale(maze_man_img, maze_man_size)
    pellet = pygame.transform.scale(pellet_img, pellet_size)
    ghost = pygame.transform.scale(ghost_img, ghost_size)

    gameDisplay = pygame.display.set_mode((display_width, display_height))
    clock = pygame.time.Clock()     # need this to set the FPS count
    pygame.display.set_caption("Maze-Man")  # game window title
    stopped = False

    def drawMazeMan(x, y):
        gameDisplay.blit(maze_man, (x, y))

    def drawGhost(x, y):
        gameDisplay.blit(ghost, (x, y))

    def drawPellets(manX, manY):
        pelletX = 50
        pelletY = 40
        while pelletX < display_width or pelletY < display_height:
            if pelletY > (manY+40) or (pelletX > (manX+5)  # check if mazeMan
                                       and pelletY == (manY+40)):  # has eaten
                gameDisplay.blit(pellet, (pelletX, pelletY))     # the pellet
            if pelletX >= display_width:  # end of row, reset X and go down
                pelletX = 50
                pelletY += 150
            else:  # Draw next pellet on the row
                pelletX += 100

    def drawTitle(title, font, color):
        titleFont = pygame.font.Font(font, 60)
        textSurface = titleFont.render(title, True, color)
        textRect = textSurface.get_rect()

        textRect.center = ((display_width/2), (display_height/2))  # centers the
        gameDisplay.blit(textSurface, textRect)                    # button

    def playButton(message, font, color, multiplier=1.0):

        playFont = pygame.font.Font(font, int(20*multiplier))  # the multiplier
        textSurface = playFont.render(message, True, color)    # creates the
        textRect = textSurface.get_rect()                      # animations

        textRect.center = ((display_width/2), 3*(display_height/4))
        gameDisplay.blit(textSurface, textRect)

        clicked = checkMouseClick(textRect.left, textRect.w, textRect.h,
                                  textRect.top)
        return clicked

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

    pygame.time.wait(1000)  # wait some time before starting the game
    while not stopped:
        gameDisplay.fill(black)

        for event in pygame.event.get():  # retrieve a list of events (clicks,.)
            if event.type == pygame.QUIT:
                stopped = True

        if current_stage == "intro sequence":
            if pygame.mouse.get_pressed()[0] == 1:
                current_stage = "menu"

            if ghostX >= display_width:  # move ghost and mazeMan to next row
                maze_manX = -30
                maze_manY += 150
                ghostX = maze_manX-150
                ghostY += 150
                if ghostY >= display_height:  # all rows have been cleared
                    current_stage = "menu"
                    maze_manY = (display_height/2) - 150  # Move the ghost off
                    ghostY = (display_height/2) - 150     # screen and the
                    ghostX = -150                         # mazeMan into place
                    pygame.time.wait(300)
                else:
                    pygame.time.wait(500)  # pause in between row changes
            else:  # Otherwise ghost and mazeMan keep moving
                maze_manX += maze_man_speed
                ghostX += ghost_speed

            drawPellets(maze_manX, maze_manY)

        elif current_stage == "menu":
            maze_manY = display_height/2 - 150
            ghostY = display_height/2 - 150
            ghostX = -100
            if maze_manX < (display_width/2 - 50):  # mazeMan enters
                maze_manX += maze_man_speed         # from the left side
            if size_multiplier > 0.9 or size_multiplier < 0.75:  # for vibrating
                size_change *= -1                                # play button
            size_multiplier += size_change

            drawTitle("MazeMan", game_title_font, yellow)
            clicked = playButton("Play", game_title_font, white,
                                 size_multiplier)
            if clicked:
                current_stage = "exit sequence"

        elif current_stage == "exit sequence":
            if ghostX <= display_width:     # In this sequence, the ghost chases
                if ghostX >= (maze_manX - 150):  # the mazeMan. But we don't
                    maze_manX += maze_man_speed  # want him to move until the
                ghostX += ghost_speed            # ghost is close enough
            else:
                pygame.time.wait(250)
                # call the main game loop here
                stopped = True

        drawMazeMan(maze_manX, maze_manY)
        drawGhost(ghostX, ghostY)
        pygame.display.update()
        clock.tick(30)  # frames per second

    pygame.quit()
    quit()


title_screen()




