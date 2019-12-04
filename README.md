# MazeMan

We are inspired by the classic, arcade game: PacMan. 

Mazeman is implemented by the language 'python' and the it's library 'pygame'.

## Game Description

The Mazeman accidently get trapped inside the maze!!

Right now he is chasing down by the ghosts!

It's up to you to save him from the maze!!

So help the mazeman to collect all the pellets and escape this maze.

## Screenshots

![giphy](https://media.giphy.com/media/PmMYKs55axgEC9Ru0X/giphy.gif)

## Controls and Features

The Mazeman is controlled by the arrow keys and wasd keys:\
w:up arrow\
a:left arrow\
s:down arrow\
d:right arrow

## How to install

### For `Windows`
1. Download Python 3 @ https://www.python.org/downloads/
2. Download Pygame @ https://www.pygame.org/download.shtml
3. Clone our projct repository @ https://github.com/williamchau123/csc290_Mazeman.git \
3.5 Download the zip file @ https://github.com/williamchau123/csc290_Mazeman/archive/master.zip
4. Run the main.py file
5. Enjoy!

## How to extend MazeMan

You may extend MazeMan by creating and adding new game elements or modifying existing elements. Here are a few simple examples.

  ### 1. Changing the speed of the ghost
  The speed of the ghost is defined in the file ```actor.py```, within the ```Ghost``` class.  To change the speed of the ghost,
  modify the ```self._delay``` attribute to the desired delay in between moves. A higher value indicates that the ghost will wait         longer before moving and will therefore be slower.
  
  ### 2. Changing the number or location of ghosts
  Each ghost actor and their location is represented as the letter 'G' within the file ```Maze-Man gameboard representation.txt```. To     remove a ghost, replace the letter 'G' with the letter 'O' (to insert a pellet) or the letter 'X' (to insert a wall). To move the       ghost, move the 'G' to your desired location while replacing the whitespace left behind with the necessary letters ('O', 'X', 'P').
  
  Note: Replacing a letter with nothing results in that spot being empty on the game stage
  
  ### 3. Changing the color of the title in the title screen
  Access the ```titleScreen.py``` file within the sampleTitleScreen folder. In that file and within the ```title_screen()``` function,     define the new color of the title according to its RGB representation. Look for the if statement that equates ```current_stage```       with "menu". Finally, in that if statement look for a line that calls the ```drawTitle()``` function and change its 3rd argument to     the new color you defined.


## Authors and Contributions

Below are the list of the authors that created this project,

We will each be talking about our contribution toward the project:

Arne Sokolovic-Created the graphical resources and designed the game stage, created a scoreboard object independent of the game's own function so as to decouple from the game engine.

Nirjari Gandhi-

Jayvin Chang- I created the title screen and victory screen for MazeMan. Additionally, I helped integrate the game stage, title screen, and victory screen elements together and ensured that they were working as intended after integration. For the README file, I wrote up the "How to extend MazeMan" section and provided a few examples of how to extend MazeMan along with it.

Jin Yoshizawa-I wrote all the docstrings in the project. To check the functionality of the game, I did multiple test plays to make sure everything is working properly. 

William Chau- I worked on the documentation for this repository such as the README and license. I also created a .gitignore file to help neglect local generated files. 



## License

The MIT License (MIT)

Copyright © 2019 Zeros_Matter

You can find a copy of the License at https://mit-license.org/

License for them is in `Public Domain`
