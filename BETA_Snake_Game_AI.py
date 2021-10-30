'''
Mini play screen 100x100: (150,210) - (400,460)

Once we have the food and head coordinates, a cue will be created of moves that bring the difference berween the coordinates closer.
The moveset will be up,down,left,right. 

'''
import numpy as np
from PIL import ImageGrab, Image, ImageOps
import matplotlib.pyplot as plot
import time
from collections import deque
from pynput.keyboard import Key, Controller

food = []
head = []
tail = [] #for simplicity, head will always be included in the tail list

game_coords = [252, 251, 499, 498] # Where the game window is on the screen.
new_path = False # This flag will trigger whenever the food has moved and we need to generate a new path.
old_screen = [item for item in np.random.rand(3,2).flatten()]  #this will start with a dummy place holder that will be checked against the first screencap.
keyboard = Controller()
start_time = time.time()
game_over = False
time.sleep(3) # make the program wait 3 seconds so you have a chance to click on the game window and make it active (for keyboard)

class SnekAI:
    def __init__(self):
        global move_que
        move_que = deque() # This queue will store our moves to the food, and will be generated each time the food is comsumed.
        self.grid()

    def grid(self):
        global num_rows, num_cols, old_screen, new_path, food, head, tail, game_over
        game_over = False
        raw_screen = ImageGrab.grab(bbox=game_coords)
        snake_screencap_grayscale = ImageOps.grayscale(raw_screen) 
        (width, height) = (10, 10)
        snake_screencap = snake_screencap_grayscale.resize((width, height), resample=0)
        screen = np.array(snake_screencap)
        screencheck = [item for item in screen.flatten()]

        if screencheck == old_screen: # If this snapshot does not contain new information, wait and try again..
            time.sleep(0.35)
            self.grid()
        elif screencheck != old_screen: # If this snapshot contains new information....
            old_screen = screencheck
            num_rows, num_cols = screen.shape # a global variable tracking the number of rows and columns in the array.
            
            # lets track where things are
            for i, node in np.ndenumerate(screen):
                coordinates = ''.join(map(str, i)) #convert the tuple to intiger
                coord = []
                for item in coordinates: # We're populating coord.
                    coord.append(int(item))
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
            if 150 not in screen.flatten(): # If the screen has no food or snake, then the game is over.
                print('GAME OVER')
                game_over = True
            #print(screen) # This line prints out the array.
            self.pathfinder()

    # Now let's determine if we need to calculate a path. A new path will be calculated when the position of the food changes.
    def pathfinder(self):
        global new_path, food, head, tail
        if new_path == False: # If the food has not moved, go on to the gameloop.
            self.gameLoop()
        elif new_path == True: # If the food has moved, calculate a new path.
            print('Finding PATH...')
            # Mode 1: shortest path
            if (len(tail)+1) < (num_rows or num_cols):
                while food != head:
                    forbidden_move = ''
                    if head[0] < food[0]: # Move Down
                        if forbidden_move != 'down':
                            move_que.append('down')
                            forbidden_move = 'up'
                            head[0] += 1
                        else:
                            pass
                    if head[0] > food[0]: # Move Up
                        if forbidden_move != 'up':
                            move_que.append('up')
                            forbidden_move = 'down'
                            head[0] -= 1
                        else:
                            pass
                    if head[1] < food[1]: # Move Right
                        if forbidden_move != 'right':
                            move_que.append('right')
                            forbidden_move = 'left'
                            head[1] += 1
                        else:
                            pass
                    if head[1] > food[1]: # Move Left
                        if forbidden_move != 'left':
                            move_que.append('left')
                            forbidden_move = 'right'
                            head[1] -= 1
                        else:
                            pass
            new_path = False
            self.gameLoop()

    # This is where we'll execute the move_que we've built in the grid method.
    def gameLoop(self):
        global game_over, food, head, tail
        while not game_over:
            try:
                move = move_que.popleft()
                if move == 'down':
                    #print('Pseudo Down')
                    keyboard.press(Key.down)
                    time.sleep(0.35)
                    keyboard.release(Key.down)
                    self.grid()
                if move == 'up':
                    #print('Pseudo Up')
                    keyboard.press(Key.up)
                    time.sleep(0.35)
                    keyboard.release(Key.up)
                    self.grid()
                if move == 'right':
                    #print('Pseudo Right')
                    keyboard.press(Key.right)
                    time.sleep(0.35)
                    keyboard.release(Key.right)
                    self.grid()
                if move == 'left':
                    #print('Pseudo Left')
                    keyboard.press(Key.left)
                    time.sleep(0.35)
                    keyboard.release(Key.left)
                    self.grid()
            except:
                print('Game Cue Empty!!!!!!')
                self.grid()
            # Exit Sequence
        if game_over == True:
            print(f'game over {move_que}')
            #move_que = deque()
            food, head, tail = [], [], [] # We're resetting everything.
            time.sleep(2)
            keyboard.press(Key.space)
            time.sleep(0.35)
            keyboard.release(Key.space)
            print('GAME OVER RESET')
            self.__init__()


snek = SnekAI()
snek