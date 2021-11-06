'''
Large play screen 800x600: (252,251) - (2249,1748) game_coords = [252, 251, 2249, 1748] # Where the game window is on the screen.

play size 300x300 

Once we have the food and head coordinates, a cue will be created of moves that bring the difference berween the coordinates closer.
The moveset will be up,down,left,right. 

Try a HILBERT curve pathfinding algorithm 

'''
import numpy as np
from math import sqrt
#import matplotlib.pyplot as plt
#from warnings import warn
#import heapq

#import multiprocessing

class SnekAI:
    def __init__(self, f_mode=3):
        self.path = []
        self.f_mode = f_mode

    def switchboard(self, res_y, res_x, forbidden_path, head, food):
        move = "Couldn't get a path to destination"
        #if len(self.path) <= 2:
        self.path = self.astar_launcher(res_y, res_x, forbidden_path, head, food)
        if self.path != 0:
            move = self.move_generator(self.path)
        #self.path.pop(0) #cut down the path by 1
        return move

    # Launch method to generate an A* path.
    def astar_launcher(self, res_y, res_x, forbidden_path, head, food):
        '''
        "1's" in the array will be interpreted as walls.
        '''
        #we're not using the maze, but passing in a blank.
        forbidden_path = np.array(forbidden_path)

        #create a maze with walls set to 1.
        maze = np.zeros((res_y, res_x), dtype= int)
        for val in forbidden_path:
            maze[val[0]][val[1]] = 1

        #plt.imshow(maze, cmap='Greys')
        #plt.show()
        
        start = tuple(head)#inputs must be tuples...
        end = tuple(food) 

        # instantiating process with arguments
        """
        num_jobs = 4
        pool = multiprocessing.Pool(processes = 4)
        input = [maze, start, end]
        mse = []
        for _ in range(num_jobs+1):
            mse.append(input)

        results = pool.map(astar_worker, mse)
        path = results[0]
        """
        path = self.astar_local(maze, start, end) #complete path to food. Note path[0] is the current head position.
        return path

    def astar_local(self, maze, start, end, allow_diagonal_movement = False):

        def return_path(current_node):
            path = []
            current = current_node
            while current is not None:
                path.append(current["position"])
                current = current["parent"]
            return path[::-1]  # Return reversed path

        # Create start and end node
        node_template = {   "parent":None,
                            "position":None,
                            "g":0,
                            "h":0,
                            "f":0
                        }

        start_node = node_template.copy()
        start_node["position"] = start

        end_node = node_template.copy()
        end_node["position"] = end

        res_y, res_x = maze.shape[0], maze.shape[1]

        # Initialize both open and closed list
        open_list = []
        closed_list = []

        max_len = 0
        max_len_node = []

        open_list.append(start_node)

        # Adding a stop condition
        outer_iterations = 0
        max_iterations = 175
        if self.f_mode == 2:
            max_iterations = 100 #Since Sqrt is slow.

        # what squares do we search
        adjacent_squares = ((-1, 0), (1, 0), (0, 1), (0, -1))
        if allow_diagonal_movement:
            adjacent_squares = ((0, -1), (0, 1), (-1, 0), (1, 0), (-1, -1), (-1, 1), (1, -1), (1, 1),)

        # Loop until you find the end
        while len(open_list) > 0:
            outer_iterations += 1
            if outer_iterations % 1000 == 0:
                print(f"Search Cycle: {outer_iterations}")

            #failed to find a path
            if outer_iterations > max_iterations:
                #warn("giving up on pathfinding too many iterations")
                #print("giving up on pathfinding too many iterations; Max Len Path chosen")
                
                val = return_path(max_len_node)
                return val
            
            # Get the current node (lowest f in the open list entries.)
            open_list.sort(key=lambda d: d['f'])
            current_node = open_list.pop(0)
            closed_list.append(current_node)

            # We're tracking longest failed path for contingency
            if len(closed_list) > max_len:
                max_len = len(closed_list)
                max_len_node = current_node.copy()

            # Found the goal
            if current_node["position"] == end_node["position"]:
                return return_path(current_node)

            # Generate children
            children = [] #This will populate with 4 adjacent nodes if valid.
            
            for new_position in adjacent_squares: # Adjacent squares

                # Get node position
                node_y, node_x = current_node["position"][0] + new_position[0], current_node["position"][1] + new_position[1]
                
                #"""
                # Make sure within range
                if node_y > (res_y-1) or node_y < 0 or node_x > (res_x-1) or node_x < 0:
                    continue

                # Make sure walkable terrain
                if maze[node_y][node_x] == 1:
                    continue

                # Create new node
                new_node= { "parent":current_node,
                            "position":(node_y, node_x),
                            "g":0,
                            "h":0,
                            "f":0
                        }

                # Append
                children.append(new_node)

            # Loop through children
            for child in children:

                # Skip if child is on the closed list
                if len([closed_child for closed_child in closed_list if closed_child["position"] == child["position"]]) > 0:
                    continue

                # Create the f, g, and h values
                child["g"] = current_node["g"] + 1
                
                if self.f_mode == 1: #cube
                    child["h"] = ((child["position"][0] - end_node["position"][0]) ** 2) + ((child["position"][1] - end_node["position"][1]) ** 2)
                elif self.f_mode == 2: #cube then sqrt
                    child["h"] = sqrt((child["position"][0] - end_node["position"][0]) ** 2) + ((child["position"][1] - end_node["position"][1]) ** 2)
                elif self.f_mode == 3: #Manhattan heuristic
                    child["h"] = 1.1*(abs(child["position"][0] - end_node["position"][0]) + abs(child["position"][1] - end_node["position"][1]))
                
                child["f"] = child["g"] + child["h"]

                # Child is already in the open list
                if len([open_node for open_node in open_list if child["position"] == open_node["position"] and child["g"] > open_node["g"]]) > 0:
                    continue

                # Add the child to the open list
                open_list.append(child)

        #warn("Couldn't get a path to destination")
        print("Couldn't get a path to destination")
        return 0

    def move_generator(self, path):
            head_coord = list(path[0])
            move_coord = list(path[1])
            move = ""
            x,y = 1,0

            if head_coord[x] != move_coord[x]: #+left/-right
                delta = head_coord[x] - move_coord[x] #+left/-right
                if delta > 0:
                    move = "Left"
                elif delta < 0:
                    move = "Right"

            elif head_coord[y] != move_coord[y]: #+up/-down
                delta = head_coord[y] - move_coord[y] #+up/-down
                if delta > 0:
                    move = "Up"
                elif delta < 0:
                    move = "Down"
            #print(head_coord, move_coord, delta)
            return move

def main():
    snek = SnekAI()
    snek.game_loop()

if __name__ == "__main__":
    main()