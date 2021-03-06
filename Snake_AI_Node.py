'''
Large play screen 800x600: (252,251) - (2249,1748) game_coords = [252, 251, 2249, 1748] # Where the game window is on the screen.

play size 300x300 

Once we have the food and head coordinates, a cue will be created of moves that bring the difference berween the coordinates closer.
The moveset will be up,down,left,right. 

Try a HILBERT curve pathfinding algorithm 

'''
import numpy as np
#import matplotlib.pyplot as plt
#from warnings import warn
import heapq

#import multiprocessing

class SnekAI:
    def __init__(self):
        self.food = []
        self.head = []
        self.tail = [] #for simplicity, head will always be included in the tail list
        self.path = []


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
        #print(f'Launching astar() with the following args;   start:{start}  end:{end}')
        #print(maze)


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

        res_y, res_x = maze.shape[0], maze.shape[1]

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
        max_iterations = 5000
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
                #print("giving up on pathfinding too many iterations; Max Len Path chosen")

                val = 0
                rand = np.random.randint(0,5)
                if rand == 0:
                    val = return_path(max_len_node)
                return val
            
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

                """
                # Make sure within range
                if node_position[0] > (len(maze) - 1) or node_position[0] < 0 or node_position[1] > (len(maze[len(maze)-1]) -1) or node_position[1] < 0:
                    continue
                """
                if (node_position[0] not in range(0, res_y)) or (node_position[1] not in range(0, res_x)):
                    continue

                # Make sure walkable terrain
                if maze[node_position[0]][node_position[1]] == 1:
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

        #warn("Couldn't get a path to destination")
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


def astar_worker(mse):
    """
    Returns a list of tuples as a path from the given start to the given end in the given maze
    :param maze:
    :param start:
    :param end:
    :return:
    """ 
    allow_diagonal_movement = False

    maze, start, end = mse[0], mse[1], mse[2]

    
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
            #print("giving up on pathfinding too many iterations; Max Len Path chosen")
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

            # Make sure walkable terrain
            if maze[node_position[0]][node_position[1]] == 1:
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

    #warn("Couldn't get a path to destination")
    return 0

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