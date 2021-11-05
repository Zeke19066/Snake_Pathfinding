'''
Controls:
    - Arrows to move
    - +/- to control game speed
Configured for 100x100 game window.


Note: Move food bool section from loop into generator function for cleanliness and to call
after each snake moves.


EVERYTHING IN Y,X FORMAT

'''
import pygame
import numpy as np
import time
import os
import Snake_AI
from collections import deque

from Custom_A_Star import pybind11module as Custom_A_Star

class SnakeGame():
    def __init__(self):
        print('Game Initialized!')
        self.ai_control = True #no human control.
        self.ai_players = 3 #how many snek?
        self.death_count = 0 #how many ded snek?

        self.resolution_width = round(3840/80)
        self.resolution_height = round(2160/80)
        self.pixel_size = 25
        self.snake_speed = 100
        self.final_speed = 0
        self.game_close = False

        self.food = []
        self.food_total_count = 0 #how many foods have we seen total?
        self.food_game_count = 0 #how many foods have we seen before we lost this game?
        self.lose_count = 0 #how many times have we lost?
        self.cycle = 1

        x, y = 100, 100
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}" # This is how we set the window position on the screen. Must come before pygame init.
        pygame.init()
        self.dis = pygame.display.set_mode((self.resolution_width*self.pixel_size, self.resolution_height*self.pixel_size))
        #self.dis = pygame.display.set_mode((self.resolution_width*self.pixel_size, self.resolution_height*self.pixel_size), pygame.FULLSCREEN)
        pygame.display.set_caption('Snake v1')

        self.screen = pygame.Surface((self.resolution_width, self.resolution_height))
        self.clock = pygame.time.Clock()
        self.font_style = pygame.font.SysFont("bahnschrift", 10)
        self.score_font = pygame.font.SysFont("consolas", 10)

        self.color_dict={
            "white": (255, 255, 255),
            "yellow": (255, 200, 50),#(255, 255, 102),
            "black": (0, 0, 0),
            "red": (213, 50, 80),
            "green": (0, 255, 0),
            "blue": (50, 153, 213),
            }

   
    def score_generator(self, score):
        value = self.score_font.render("Your Score: " + str(score), True, self.color_dict["white"])
        self.screen.blit(value, [0, 0]) # Draw the score onto the screen at these coordinates.

    def snake_plotter(self, snake_player):
        for pixel in snake_player.full_snek:
            pygame.draw.rect(self.screen, snake_player.color, [pixel[1], pixel[0], 1, 1])

    def message(self, msg, color):
        mesg = self.font_style.render(msg, True, color)
        #self.screen.blit(mesg, [int(self.resolution_width / 6), int(self.resolution_height / 3)])
        self.screen.blit(mesg, [0, int(self.resolution_height / 3)])

    def food_generator(self):
        forbidden_spawn = self.forbidden_builder("Spawn")

        self.food = forbidden_spawn[0]
        while self.food in forbidden_spawn:
            self.food=[]
            foodx = np.random.randint(0, self.resolution_width)
            foody = np.random.randint(0, self.resolution_height)
            self.food = [foody, foodx]

        self.player_1.food = self.food
        if self.ai_players == 2:
            self.player_2.food = self.food
        if self.ai_players == 3:
            self.player_2.food = self.food
            self.player_3.food = self.food

        self.food_game_count += 1
        self.food_total_count += 1

        pygame.draw.rect(self.screen, self.color_dict["red"], [foodx, foody, 1, 1])
        self.dis.blit(pygame.transform.scale(self.screen, self.dis.get_rect().size), (0, 0))
        pygame.display.update()

        #Call Snake Plotter for every snake.
        self.snake_plotter(self.player_1)
        if self.ai_players == 2:
            self.snake_plotter(self.player_2)
        if self.ai_players == 3:
            self.snake_plotter(self.player_2)
            self.snake_plotter(self.player_3)

    def gameLoop(self):
        speed_mod = 0 # Speed adjustments made after the game has started.
        terminal_bool = False
        self.player_1 = Snek_Actor(self.color_dict["green"], 1, self.resolution_width, self.resolution_height)
        if self.ai_players == 2:
            self.player_2 = Snek_Actor(self.color_dict["blue"], 2, self.resolution_width, self.resolution_height)
        if self.ai_players == 3:
            self.player_2 = Snek_Actor(self.color_dict["blue"], 2, self.resolution_width, self.resolution_height)
            self.player_3 = Snek_Actor(self.color_dict["yellow"], 3, self.resolution_width, self.resolution_height)
        self.food_generator() #this is when we request the starting food.


        while not terminal_bool:
            food_bool = False
            dead_count = 0

            # Exit Sequence
            if self.game_close == True:
                self.screen.fill(self.color_dict["black"])
                self.message("Press Space or Esc", self.color_dict["white"])
                #self.score_generator(snake_length - 1)
                self.dis.blit(pygame.transform.scale(self.screen, self.dis.get_rect().size), (0, 0))
                pygame.display.update()
                self.lose_count += 1
                print(f'lose count:{self.lose_count};  food count:{self.food_game_count-1};   total food count:{self.food_total_count-1}')
                self.food_game_count = 0
                while self.game_close == True:
                    
                    if self.ai_control:
                        #time.sleep(1)
                        self.game_close = False
                        self.gameLoop()

                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                print('Exiting Now')
                                terminal_bool = True
                                self.game_close = False
                            if event.key == pygame.K_SPACE:
                                self.game_close = False
                                self.gameLoop()
            
            #process user input
            if not self.ai_control:
                for event in pygame.event.get():
                    #print(event)
                    if event.type == pygame.QUIT:
                        terminal_bool = True
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_LEFT:
                            x1_change = -1
                            y1_change = 0
                        elif event.key == pygame.K_RIGHT:
                            x1_change = 1
                            y1_change = 0
                        elif event.key == pygame.K_UP:
                            y1_change = -1
                            x1_change = 0
                        elif event.key == pygame.K_DOWN:
                            y1_change = 1
                            x1_change = 0
                        
                        elif event.key == pygame.K_KP_PLUS:
                            speed_mod += 1
                        elif event.key == pygame.K_KP_MINUS:
                            speed_mod -= 1
                
            #process ai control
            if self.ai_control and (self.cycle!=1):
                #First process user quit command if preset.
                for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            terminal_bool = True
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                print('Exiting Now')
                                terminal_bool = True
                                self.game_close = False

                #now run the AI stuff
                forbidden_path = self.forbidden_builder("Path", player=1)
                food_bool = self.player_1.snek_step(forbidden_path)
                dead_count += self.player_1.dead_bool
                if food_bool:#trigger the new food condition
                    self.food_generator()  # We generate the next food before updating the screen.
                
                if self.ai_players == 2:
                    forbidden_path = self.forbidden_builder("Path", player=2)
                    food_bool = self.player_2.snek_step(forbidden_path)
                    dead_count += self.player_1.dead_bool
                    if food_bool:#trigger the new food condition
                        self.food_generator()  # We generate the next food before updating the screen.
                if self.ai_players == 3:
                    forbidden_path = self.forbidden_builder("Path", player=2)
                    food_bool = self.player_2.snek_step(forbidden_path)
                    dead_count += self.player_2.dead_bool
                    if food_bool:#trigger the new food condition
                        self.food_generator()  # We generate the next food before updating the screen.
                    forbidden_path = self.forbidden_builder("Path", player=3)
                    food_bool = self.player_3.snek_step(forbidden_path)
                    dead_count += self.player_3.dead_bool
                    if food_bool:#trigger the new food condition
                        self.food_generator()  # We generate the next food before updating the screen.


            self.screen.fill(self.color_dict["black"])
            pygame.draw.rect(self.screen, self.color_dict["red"], [self.food[1], self.food[0], 1, 1])
            
            #Call Snake Plotter for every snake.
            self.snake_plotter(self.player_1)
            if self.ai_players == 2:
                self.snake_plotter(self.player_2)
            if self.ai_players == 3:
                self.snake_plotter(self.player_2)
                self.snake_plotter(self.player_3)

            if dead_count == self.ai_players: #All snek ded
                    time.sleep(3) #bask in the snek
                    self.game_close = True

            #self.score_generator(snake_length - 1)
            self.dis.blit(pygame.transform.scale(self.screen, self.dis.get_rect().size), (0, 0))
            pygame.display.update()
            
            self.final_speed = self.snake_speed+speed_mod
            self.clock.tick(self.final_speed)
            self.cycle += 1
            #pygame.image.save(self.dis,"screenshot.png")
    
        pygame.quit()
        quit()

    def forbidden_builder(self, mode, player=0):
        #spawn includes all occupied squares; path excludes head & food

        forbidden_list = []

        if mode == "Spawn":
            forbidden_list += self.player_1.full_snek
            if self.ai_players == 2:
                forbidden_list += self.player_2.full_snek
            if self.ai_players == 3:
                forbidden_list += self.player_2.full_snek
                forbidden_list += self.player_3.full_snek
            forbidden_list += self.food

        elif mode == "Path":
            if player == 1:
                forbidden_list += list(self.player_1.body) #just the body
            elif player != 1:
                forbidden_list += self.player_1.full_snek #full snek
            
            if self.ai_players == 2:
                if player == 2:
                    forbidden_list += list(self.player_2.body) #just the body
                elif player != 2:
                    forbidden_list += self.player_2.full_snek #full snek
            
            if self.ai_players == 3:
                if player == 2:
                    forbidden_list += list(self.player_2.body) #just the body
                elif player != 2:
                    forbidden_list += self.player_2.full_snek #full snek
                if player == 3:
                    forbidden_list += list(self.player_3.body) #just the body
                elif player != 3:
                    forbidden_list += self.player_3.full_snek #full snek
                        
        return forbidden_list

class Snek_Actor():
    def __init__(self, color, player_num, resolution_width, resolution_height):
        self.color = color
        self.player_num = player_num
        self.resolution_height = resolution_height
        self.resolution_width = resolution_width
        self.dead_bool = False
        self.py_ai = Snake_AI.SnekAI()

        self.x1 = np.random.randint(1,self.resolution_width-1)
        self.y1 = np.random.randint(1,self.resolution_height-1)
        self.x1_change = 0
        self.y1_change = 0
        self.last_action = "Left"

        self.food = [] #this will be overwritten each time food is spawned.
        self.snek_length = 0 #Note!!!! doesnt count the head!
        self.head = [self.y1, self.x1]
        self.body = deque(maxlen=self.snek_length) #initialized empty.
        self.full_snek = list(self.body.copy()) #a combination of body and head.
        self.full_snek.append(self.head)

    def snek_step(self, forbidden_path):
        """
        Collision is determined here
        forbidden_spawn contains all occupied coords except head & food (start & finish)
        if we got the food, that's determined here.
        """
        food_bool = False
        #if we're dead, do nothing.
        if self.dead_bool:
            return food_bool

        if forbidden_path == []:
            forbidden_path = [[0,0]]

        """
        action = Custom_A_Star.launcher(self.resolution_height, self.resolution_width,
                                    forbidden_path, self.head, self.food)
        """

        #'''
        action =self.py_ai.switchboard(self.resolution_height, self.resolution_width,
                                    forbidden_path, self.head, self.food)
        #'''

        if len(action) > 6:
            #print(f"{self.player_num}  {action}  Head:{self.head}   Food:{self.food}  {forbidden_path}")
            #print(action)
            action = self.last_action

        if action == "Left":
            x1_change = -1
            y1_change = 0
        elif action == "Right":
            x1_change = 1
            y1_change = 0
        elif action == "Up":
            y1_change = -1
            x1_change = 0
        elif action == "Down":
            y1_change = 1
            x1_change = 0

        #add old head to the body que; nulls if length equals zero.
        if self.snek_length > 0:
            self.body.append(self.head.copy())

        #apply the modification to head position.
        self.head[1] += x1_change
        self.head[0] += y1_change
        if self.head[1] not in range(0, self.resolution_width):
            self.dead_bool = True
            self.color = (150, 150, 150) #ghost
            if len(self.body)>0:
                self.head = self.body[0] #reset to last head that is in-bounds
            elif len(self.body)==0:
                self.head[1] -= x1_change
                self.head[0] -= y1_change
            return food_bool
        if self.head[0] not in range(0, self.resolution_height):
            self.dead_bool = True
            self.color = (150, 150, 150) #ghost
            if len(self.body)>0:
                self.head = self.body[0] #reset to last head that is in-bounds
            elif len(self.body)==0:
                self.head[1] -= x1_change
                self.head[0] -= y1_change
            return food_bool
        if self.head in forbidden_path:
            self.dead_bool = True
            self.color = (150, 150, 150) #ghost
            if len(self.body)>0:
                self.head = self.body[0] #reset to last head that is in-bounds
            elif len(self.body)==0:
                self.head[1] -= x1_change
                self.head[0] -= y1_change
            return food_bool


        #we got the food; snek gets longer
        if self.head == self.food:
            food_bool = True #will trigger new food.
            self.snek_length += 1
            temp = list(self.body.copy())
            self.body = deque(temp, maxlen=self.snek_length)

        self.full_snek = list(self.body.copy()) #a combination of body and head.
        self.full_snek.append(self.head.copy())
        self.last_action = action

        return food_bool

def main():
    snek = SnakeGame()
    snek.gameLoop()

if __name__ == "__main__":
    main()