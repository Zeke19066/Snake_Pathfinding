'''
Controls:
    - Arrows to move
    - +/- to control game speed
Configured for 100x100 game window.
'''
import pygame
import time
import random
from random import choice
import os

resolution_width = 300
resolution_height = 300
block_size = 10
snake_speed = 3
final_speed = 0
game_close = False

snake_Head = []
snake_List = []
food = []
food_total_count = 0 #how many foods have we seen total?
food_game_count = 0 #how many foods have we seen before we lost this game?
lose_count = 0 #how many times have we lost?

x, y = 100, 100
os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (x,y) # This is how we set the window position on the screen. Must come before pygame init.
pygame.init()
dis = pygame.display.set_mode((resolution_width, resolution_height))
pygame.display.set_caption('Snake v1')
clock = pygame.time.Clock()
font_style = pygame.font.SysFont("bahnschrift", 10)
score_font = pygame.font.SysFont("consolas", 10)

white = (255, 255, 255)
yellow = (255, 255, 102)
black = (0, 0, 0)
red = (213, 50, 80)
green = (0, 255, 0)
blue = (50, 153, 213)

class SnakeGame():
    def __init__(self):
        print('Game Initialized!')
        self.gameLoop()

    def score_generator(self, score):
        value = score_font.render("Your Score: " + str(score), True, white)
        dis.blit(value, [0, 0]) # Draw the score onto the screen at these coordinates.

    def snake_plotter(self, block_size, snake_list):
        for x in snake_list:
            pygame.draw.rect(dis, green, [x[0], x[1], block_size, block_size])

    def message(self, msg, color):
        mesg = font_style.render(msg, True, color)
        #dis.blit(mesg, [int(resolution_width / 6), int(resolution_height / 3)])
        dis.blit(mesg, [0, int(resolution_height / 3)])

    def food_generator(self, snake_List):
        global food_game_count, food_total_count
        food_xy = []
        foodx = round(random.randrange(0, resolution_width - block_size, block_size))
        foody = round(random.randrange(0, resolution_height - block_size, block_size))
        food_xy.append(foodx)
        food_xy.append(foody)
        if food_xy in snake_List:
            return self.food_generator(snake_List)
        elif food_xy not in snake_List:
            self.food = food_xy #let's update the global variable for export to the AI.
            food_game_count += 1
            food_total_count += 1
            return foodx, foody

    def gameLoop(self):
        global food_game_count, food_total_count, lose_count, game_close
        speed_mod = 0 # Speed adjustments made after the game has started.
        game_over = False
        x1 = resolution_width //2
        y1 = resolution_height // 2
        x1_change = 0
        y1_change = 0
        snake_List = []
        Length_of_snake = 1
        foodx, foody = self.food_generator(snake_List) #this is when we request the starting food.
    
        while not game_over:
            # Exit Sequence
            if game_close == True:
                dis.fill(black)
                self.message("Press Space or Esc", white)
                self.score_generator(Length_of_snake - 1)
                pygame.display.update()
                lose_count += 1
                print(f'lose count:{lose_count};  food count:{food_game_count-1};   total food count:{food_total_count-1}')
                food_game_count = 0
                while game_close == True:
                    for event in pygame.event.get():
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_ESCAPE:
                                print('Exiting Now')
                                game_over = True
                                game_close = False
                            if event.key == pygame.K_SPACE:
                                game_close = False
                                self.gameLoop()
            for event in pygame.event.get():
                #print(event)
                if event.type == pygame.QUIT:
                    game_over = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        x1_change = -block_size
                        y1_change = 0
                    elif event.key == pygame.K_RIGHT:
                        x1_change = block_size
                        y1_change = 0
                    elif event.key == pygame.K_UP:
                        y1_change = -block_size
                        x1_change = 0
                    elif event.key == pygame.K_DOWN:
                        y1_change = block_size
                        x1_change = 0
                    
                    elif event.key == pygame.K_KP_PLUS:
                        speed_mod += 1
                    elif event.key == pygame.K_KP_MINUS:
                        speed_mod -= 1
            if (x1 >= resolution_width or x1 < 0) or (y1 >= resolution_height or y1 < 0):
                game_close = True
                self.gameLoop()
            
            x1 += x1_change
            y1 += y1_change
            dis.fill(black)
            pygame.draw.rect(dis, red, [foodx, foody, block_size, block_size])
            snake_Head = []
            snake_Head.append(x1)
            snake_Head.append(y1)
            self.snake_Head = snake_Head #let's update the global variable for export to the AI.
            snake_List.append(snake_Head)
            if len(snake_List) > Length_of_snake:
                del snake_List[0]
            self.snake_List = snake_List #let's update the global variable for export to the AI.
            # SELF-CRASH: Last entry (:-1) is the head position. If a segment's coordinates match the head's coordinates, Game Over.
            for x in snake_List[:-1]:
                if x == snake_Head:
                    game_close = True
            self.snake_plotter(block_size, snake_List)
            #self.score_generator(Length_of_snake - 1)
            pygame.display.update()
            if x1 == foodx and y1 == foody:
                foodx, foody = self.food_generator(snake_List)  # We generate the next food before updating the screen.
                pygame.draw.rect(dis, red, [foodx, foody, block_size, block_size])
                pygame.display.update()
                Length_of_snake += 1
            final_speed = snake_speed+speed_mod
            clock.tick(final_speed)
    
        pygame.quit()
        quit()

snek = SnakeGame()
snek