'''
Large play screen 800x600: (252,251) - (2249,1748) game_coords = [252, 251, 2249, 1748] # Where the game window is on the screen.

play size 300x300 

Once we have the food and head coordinates, a cue will be created of moves that bring the difference berween the coordinates closer.
The moveset will be up,down,left,right. 

Try a HILBERT curve pathfinding algorithm 

'''
import numpy as np
from PIL import ImageGrab, Image, ImageOps
import matplotlib.pyplot as plot
import time
from collections import deque
from pynput.keyboard import Key, Controller
import gc # for recursion problems....

food = []
head = []
tail = [] #for simplicity, head will always be included in the tail list

res_x = 300
res_y = 300
block_size = 10

game_coords = [252, 251, 999, 998] # Where the game window is on the screen.
new_path = False # This flag will trigger whenever the food has moved and we need to generate a new path.
old_screen = [item for item in np.random.rand(3,2).flatten()]  #this will start with a dummy place holder that will be checked against the first screencap.
screencheck = old_screen
keyboard = Controller()
start_time = time.time()
game_over = False
time.sleep(3) # make the program wait 3 seconds so you have a chance to click on the game window and make it active (for keyboard)
next_coord = ''


class SnekAI:
    def __init__(self):
        global move_que
        move_que = deque() # This queue will store our moves to the food, and will be generated each time the food is comsumed.
        self.screen_grid()

    # This will generate a grayscale array at a resolution of 1block/pixel; will populate the head, tail, and food lists based on array.
    def screen_grid(self):
        global num_rows, num_cols, old_screen, new_path, food, head, tail, game_over, screencheck, block_size, res_x, res_y
        gc.collect()
        print(f'screen_grid() started')
        game_over = False

        while screencheck == old_screen: # If this snapshot does not  contain new information, wait and try again..
            time.sleep(0.05)
            raw_screen = ImageGrab.grab(bbox=game_coords)
            snake_screencap_grayscale = ImageOps.grayscale(raw_screen) 
            (width, height) = (int(res_x/block_size), int(res_y/block_size))
            snake_screencap = snake_screencap_grayscale.resize((width, height), resample=0)
            screen = np.array(snake_screencap)
            #print(screen)
            screencheck = [item for item in screen.flatten()]

        if screencheck != old_screen: # If this snapshot contains new information....
            old_screen = screencheck
            num_rows, num_cols = screen.shape # a global variable tracking the number of rows and columns in the array.
            
            print(f'New Screen Detected, Analyzing')
            # Update head, tail, food with block coordinates.
            for i, node in np.ndenumerate(screen):
                coord = [int(n) for n in i] # Pesky tuples

                if node == 0:
                    if coord in tail:
                        del tail[0]
                if node == 102: # the food (red pixel) greyscale value.
                    if coord != food:
                        food = coord
                        new_path = True
                        print(f'NEW FOOD: {food}')
                if node == 150: # the head & tail (green pixel) greyscale value.
                    if coord not in tail:
                        tail.append(coord)
                        head = coord
            if 150 not in screen.flatten(): # If the snake isn't on screen, the game is over.
                print('GAME OVER')
                game_over = True
            elif 102 not in screen.flatten(): # Sometimes the food takes a sec to generate. This skips until we see new food.
                print(f'No Food! Pausing 1/10 sec & retest')
                time.sleep(0.05)
                self.screen_grid()
            #print(screen) # This line prints out the array.
            print(f'screen_grid() END, jumping to switchboard()')
            self.switchboard()

    # This function will generate the A* path coordinates based on the launch method astar_launcher.
    def astar(self, maze, start, end):
        """Returns a list of tuples as a path from the given start to the given end in the given maze"""
        # Create start and end node
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        # Add the start node
        open_list.append(start_node)

        # Loop until you find the end
        while len(open_list) > 0:

            # Get the current node
            current_node = open_list[0]
            current_index = 0
            for index, item in enumerate(open_list):
                if item.f < current_node.f:
                    current_node = item
                    current_index = index

            # Pop current off open list, add to closed list
            open_list.pop(current_index)
            closed_list.append(current_node)

            # Found the goal
            if current_node == end_node:
                path = []
                current = current_node
                while current is not None:
                    path.append(current.position)
                    current = current.parent
                return path[::-1] # Return reversed path

            # Generate children
            children = []
            for new_position in [(0, -1), (0, 1), (-1, 0), (1, 0)]: # Adjacent squares, daigonals forbidden.

                # Get node position
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range
                if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                    continue

                # Make sure walkable terrain
                if maze[node_position[0]][node_position[1]] != 0:
                    continue

                # Create new node
                new_node = Node(current_node, node_position)

                # Append
                children.append(new_node)

            # Loop through children
            for child in children:

                # Child is on the closed list
                for closed_child in closed_list:
                    if child == closed_child:
                        continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                # Child is already in the open list
                for open_node in open_list:
                    if child == open_node and child.g > open_node.g:
                        continue

                # Add the child to the open list
                open_list.append(child)

    # Launch method to generate an A* path.
    def astar_launcher(self):
        global next_coord
        '''
        "1's" in the array will be interpreted as walls.
        '''
        maze = np.zeros((num_rows, num_cols), dtype= int)

        # We put a 1 where the body lies.
        for i, node in np.ndenumerate(maze):
            int_i = [int(n) for n in i] # Pesky tuples
            x,y = int_i[0], int_i[1]
            if (int_i != head) and (int_i in tail):
                maze[x][y] = 1  
        start = tuple(head)#inputs must be tuples...
        end = tuple(food) 
        print(f'Launching astar() with the following args;   start:{start}  end:{end}')
        #print(maze)
        path = self.astar(maze, start, end)
        next_coord = path[1] #just the next move. Note the element in the set (path[0]) is the start position.
        print(f'A* path found; next coord is: {next_coord}')
        self.gameLoop()

    # This is the switcboard for the pathfinding algorithm we execute.
    def switchboard(self):

        global new_path, food, head, tail
        if new_path == False: # If the food has not moved, go on to the gameloop.
            self.gameLoop()

        elif new_path == True: # If the food has moved, calculate a new path.
            print('Finding PATH...')
            if (len(tail)+1) < (num_rows or num_cols): # If tail length less than either height OR width, use A* Path
                print(f'A* PATH selected, jumping to astar_launcher()')
                self.astar_launcher()
            new_path = False
            self.gameLoop()

    # This is where we'll execute the move based on our pathfinding output.
    def gameLoop(self):
        global game_over, food, head, tail, next_coord
        forbidden_move = '' # If we are adjacent to a wall, we cannot move towards the wall (or else game over). This forbidden move will be stored here.


        print(f'____________________________________________________________starting gameLoop()')
        while not game_over:
            int_next_coord = [int(n) for n in next_coord] # Pesky tuples
            print(f'int_next_coord: {int_next_coord};   head:{head}')

            '''
            #This is where we make sure we cannot move off the screen.
            if head[0] == 1: # We're on the left wall
                forbidden_move = 'left'
                continue
            if head[0] == (num_cols-1): # We're on the right wall
                forbidden_move = 'right'
                continue
            if head[1] == 1: # We're on the top wall
                forbidden_move = 'top'
                continue
            if head[1] == (num_rows-1): # We're on the bottom wall
                forbidden_move = 'bottom'
                continue
            print(forbidden_move)
            '''

            if head[0] < int_next_coord[0]: # Move Down
                print('Pseudo Down')
                keyboard.press(Key.down)
                time.sleep(0.1)
                keyboard.release(Key.down)
                self.screen_grid()
            if head[0] > int_next_coord[0]: # Move Up
                print('Pseudo Up')
                keyboard.press(Key.up)
                time.sleep(0.1)
                keyboard.release(Key.up)
                self.screen_grid()
            
            if head[0] == int_next_coord[0]: # Let's take a lateral move.
                if head[1] < int_next_coord[1]: # Move Right
                    print('Pseudo Right')
                    keyboard.press(Key.right)
                    time.sleep(0.1)
                    keyboard.release(Key.right)
                    self.screen_grid()
                if head[1] > int_next_coord[1]: # Move Left
                    print('Pseudo Left')
                    keyboard.press(Key.left)
                    time.sleep(0.1)
                    keyboard.release(Key.left)
                    self.screen_grid()

            print('Something went wrong in the game loop!')
            self.screen_grid()
            # Exit Sequence
        if game_over == True:
            food, head, tail = [], [], [] # We're resetting everything.
            time.sleep(2)
            keyboard.press(Key.space)
            time.sleep(0.35)
            keyboard.release(Key.space)
            print('GAME OVER RESET')
            self.__init__()

class Node():
    """A node class for A* Pathfinding"""

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position

snek = SnekAI()
snek