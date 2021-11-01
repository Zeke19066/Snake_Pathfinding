'''
Large play screen 800x600: (252,251) - (2249,1748) game_coords = [252, 251, 2249, 1748] # Where the game window is on the screen.

play size 300x300 

Once we have the food and head coordinates, a cue will be created of moves that bring the difference berween the coordinates closer.
The moveset will be up,down,left,right. 

Try a HILBERT curve pathfinding algorithm 

'''
import numpy as np
import cv2
import matplotlib.pyplot as plt
import time
from pynput.keyboard import Key, Controller
from warnings import warn
import heapq



class SnekAI:
    def __init__(self):
        self.food = []
        self.head = []
        self.tail = [] #for simplicity, head will always be included in the tail list
        self.path = []

        self.start_time = time.time()
        #time.sleep(3) # make the program wait 3 seconds so you have a chance to click on the game window and make it active (for keyboard)
        self.next_coord = []
        self.first_move = True

    def switchboard(self, screen_array):
        move = ""
        self.screen_grid(screen_array)
        #if len(self.path) <= 2:
        self.path = self.astar_launcher()
        if self.path != 0:
            move = self.move_generator(self.path)
        #self.path.pop(0) #cut down the path by 1
        return move

    # This will generate a grayscale array at a resolution of 1block/pixel; will populate the head, tail, and food lists based on array.
    def screen_grid(self, screen):
            screen = cv2.cvtColor(screen, cv2.COLOR_RGB2GRAY)
            #plt.imshow(screen, cmap="gray")
            #plt.show()
            self.num_rows, self.num_cols = screen.shape # a global variable tracking the number of rows and columns in the array.
            #print(f'New Screen Detected, Analyzing')
            # Update head, tail, food with block coordinates.
            for coord, pixel in np.ndenumerate(screen):
                coord = list(coord) # Pesky tuples
                if pixel == 0:
                    if coord in self.tail:
                        i = self.tail.index(coord)
                        del self.tail[i]
                if pixel == 102: # the food (red pixel) greyscale value.
                    if coord != self.food:
                        self.food = coord
                        #print(f'NEW FOOD: {food}')
                if pixel == 150: # the head & tail (green pixel) greyscale value.
                    if coord not in self.tail:
                        self.tail.append(coord)
                        self.head = coord
            if 150 not in screen.flatten(): # If the snake isn't on screen, the game is over.
                print('GAME OVER')
            if 102 not in screen.flatten(): # Sometimes the food takes a sec to generate. This skips until we see new food.
                time.sleep(0.01)
            return

    # Launch method to generate an A* path.
    def astar_launcher(self):
        '''
        "1's" in the array will be interpreted as walls.
        '''
        #we're not using the maze, but passing in a blank.
        maze = np.zeros((self.num_rows, self.num_cols), dtype= int)
        
        #plt.imshow(maze, cmap='Greys')
        #plt.show()
        
        start = tuple(self.head)#inputs must be tuples...
        end = tuple(self.food) 
        #print(f'Launching astar() with the following args;   start:{start}  end:{end}')
        #print(maze)
        path = self.astar(maze, start, end) #complete path to food. Note path[0] is the current head position.

        return path

    def astar(self, maze, start, end, allow_diagonal_movement = False):
        """
        Returns a list of tuples as a path from the given start to the given end in the given maze
        :param maze:
        :param start:
        :param end:
        :return:
        """
        def return_path(current_node):
            path = []
            current = current_node
            while current is not None:
                path.append(current.position)
                current = current.parent
            return path[::-1]  # Return reversed path

        # Create start and end node
        start_node = Node(None, start)
        start_node.g = start_node.h = start_node.f = 0
        end_node = Node(None, end)
        end_node.g = end_node.h = end_node.f = 0

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        max_len = 0
        max_len_node = []

        # Heapify the open_list and Add the start node
        heapq.heapify(open_list) 
        heapq.heappush(open_list, start_node)

        # Adding a stop condition
        outer_iterations = 0

        #max_iterations = (len(maze[0]) * len(maze) * 10)
        #max_iterations = (len(maze[0]) * len(maze) // 2)
        #max_iterations = (len(maze[0]) * len(maze))
        #max_iterations = (len(maze[0]) * len(maze[1]))
        max_iterations = 100

        # what squares do we search
        adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0))
        if allow_diagonal_movement:
            adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1),)

        # Loop until you find the end
        while len(open_list) > 0:
            outer_iterations += 1
            if outer_iterations % 1000 == 0:
                print(f"Search Cycle: {outer_iterations}")
            #print(outer_iterations)

            #failed to find a path
            if outer_iterations > max_iterations:
                #warn("giving up on pathfinding too many iterations")
                print("giving up on pathfinding too many iterations; Max Len Path chosen")
                return return_path(max_len_node)
            
            # Get the current node
            current_node = heapq.heappop(open_list)
            closed_list.append(current_node)

            # We're tracking longest failed path for contingency
            if len(closed_list) > max_len:
                max_len = len(closed_list)
                max_len_node = current_node

            # Found the goal
            if current_node == end_node:
                return return_path(current_node)

    
            # Generate children
            children = []
            
            for new_position in adjacent_squares: # Adjacent squares

                # Get node position
                node_position = (current_node.position[0] + new_position[0], current_node.position[1] + new_position[1])

                # Make sure within range
                if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                    continue

                """
                # Make sure walkable terrain
                if maze[node_position[0]][node_position[1]] != 0:
                    continue
                """

                if list(node_position) in self.tail:
                    continue

                # Create new node
                new_node = Node(current_node, node_position)

                # Append
                children.append(new_node)

            # Loop through children
            for child in children:
                # Child is on the closed list
                if len([closed_child for closed_child in closed_list if closed_child == child]) > 0:
                    continue

                # Create the f, g, and h values
                child.g = current_node.g + 1
                child.h = ((child.position[0] - end_node.position[0]) ** 2) + ((child.position[1] - end_node.position[1]) ** 2)
                child.f = child.g + child.h

                # Child is already in the open list
                if len([open_node for open_node in open_list if child.position == open_node.position and child.g > open_node.g]) > 0:
                    continue

                # Add the child to the open list
                heapq.heappush(open_list, child)

        warn("Couldn't get a path to destination")
        return 0

    def move_generator(self, path):
            head_coord = list(path[0])
            move_coord = list(path[1])
            move = ""

            if head_coord[0] != move_coord[0]: #+left/-right
                delta = head_coord[0] - move_coord[0] #+left/-right
                if delta > 0:
                    move = "Left"
                elif delta < 0:
                    move = "Right"

            elif head_coord[1] != move_coord[1]: #+up/-down
                delta = head_coord[1] - move_coord[1] #+up/-down
                if delta > 0:
                    move = "Up"
                elif delta < 0:
                    move = "Down"
            #print(head_coord, move_coord, delta)
            return move

class Node:
    """
    A node class for A* Pathfinding
    """

    def __init__(self, parent=None, position=None):
        self.parent = parent
        self.position = position

        self.g = 0
        self.h = 0
        self.f = 0

    def __eq__(self, other):
        return self.position == other.position
    
    def __repr__(self):
      return f"{self.position} - g: {self.g} h: {self.h} f: {self.f}"

    # defining less than for purposes of heap queue
    def __lt__(self, other):
      return self.f < other.f
    
    # defining greater than for purposes of heap queue
    def __gt__(self, other):
      return self.f > other.f

def main():
    snek = SnekAI()
    snek.game_loop()

if __name__ == "__main__":
    main()