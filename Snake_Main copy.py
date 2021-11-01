'''
Controls:
    - Arrows to move
    - +/- to control game speed
Configured for 100x100 game window.
'''
import pygame
import time
import random
import os
import Snake_Game_AI as AI

class SnakeGame():
    def __init__(self):
        print('Game Initialized!')
        self.ai_control = True #no human control.
        self.ai = AI.SnekAI()
        self.resolution_width = 500
        self.resolution_height = 500
        self.block_size = 10
        self.snake_speed = 500
        self.final_speed = 0
        self.game_close = False

        self.snake_Head = []
        self.snake_Body = []
        self.food = []
        self.food_total_count = 0 #how many foods have we seen total?
        self.food_game_count = 0 #how many foods have we seen before we lost this game?
        self.lose_count = 0 #how many times have we lost?
        self.cycle = 1

        x, y = 100, 100
        os.environ['SDL_VIDEO_WINDOW_POS'] = f"{x},{y}" # This is how we set the window position on the screen. Must come before pygame init.
    
        pygame.init()
        self.dis = pygame.display.set_mode((self.resolution_width, self.resolution_height))
        pygame.display.set_caption('Snake v1')
        self.clock = pygame.time.Clock()
        self.font_style = pygame.font.SysFont("bahnschrift", 10)
        self.score_font = pygame.font.SysFont("consolas", 10)

        self.color_dict={
            "white": (255, 255, 255),
            "yellow": (255, 255, 102),
            "black": (0, 0, 0),
            "red": (213, 50, 80),
            "green": (0, 255, 0),
            "blue": (50, 153, 213),
            }

        
    def score_generator(self, score):
        value = self.score_font.render("Your Score: " + str(score), True, self.color_dict["white"])
        self.dis.blit(value, [0, 0]) # Draw the score onto the screen at these coordinates.

    def snake_plotter(self):
        for x in self.snake_Body:
            pygame.draw.rect(self.dis, self.color_dict["green"], [x[0], x[1], self.block_size, self.block_size])

    def message(self, msg, color):
        mesg = self.font_style.render(msg, True, color)
        #self.dis.blit(mesg, [int(self.resolution_width / 6), int(self.resolution_height / 3)])
        self.dis.blit(mesg, [0, int(self.resolution_height / 3)])

    def food_generator(self):
        food_xy = []
        foodx = round(random.randrange(0, self.resolution_width - self.block_size, self.block_size))
        foody = round(random.randrange(0, self.resolution_height - self.block_size, self.block_size))
        food_xy.append(foodx)
        food_xy.append(foody)
        if food_xy in self.snake_Body:
            return self.food_generator()
        elif food_xy not in self.snake_Body:
            self.food = food_xy #let's update the global variable for export to the AI.
            self.food_game_count += 1
            self.food_total_count += 1
            return foodx, foody

    def gameLoop(self):
        speed_mod = 0 # Speed adjustments made after the game has started.
        terminal_bool = False
        x1 = self.resolution_width //2
        y1 = self.resolution_height //2
        x1_change = 0
        y1_change = 0
        self.snake_Body = []
        snake_length = 1
        foodx, foody = self.food_generator() #this is when we request the starting food.

        while not terminal_bool:
            x1_change, y1_change = 0,0

            # Exit Sequence
            if self.game_close == True:
                self.dis.fill(self.color_dict["black"])
                self.message("Press Space or Esc", self.color_dict["white"])
                self.score_generator(snake_length - 1)
                pygame.display.update()
                self.lose_count += 1
                print(f'lose count:{self.lose_count};  food count:{self.food_game_count-1};   total food count:{self.food_total_count-1}')
                self.food_game_count = 0
                while self.game_close == True:
                    if self.ai_control:
                        time.sleep(1)
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
                            x1_change = -self.block_size
                            y1_change = 0
                        elif event.key == pygame.K_RIGHT:
                            x1_change = self.block_size
                            y1_change = 0
                        elif event.key == pygame.K_UP:
                            y1_change = -self.block_size
                            x1_change = 0
                        elif event.key == pygame.K_DOWN:
                            y1_change = self.block_size
                            x1_change = 0
                        
                        elif event.key == pygame.K_KP_PLUS:
                            speed_mod += 1
                        elif event.key == pygame.K_KP_MINUS:
                            speed_mod -= 1
                
            #process ai control
            if self.ai_control and (self.cycle!=1):
                screen_array = pygame.surfarray.array3d(self.dis) 
                #print(screen_array.shape)

                action = self.ai.switchboard(screen_array, self.block_size)
                #print(action)
                if action == "Left":
                    x1_change = -self.block_size
                    y1_change = 0
                elif action == "Right":
                    x1_change = self.block_size
                    y1_change = 0
                elif action == "Up":
                    y1_change = -self.block_size
                    x1_change = 0
                elif action == "Down":
                    y1_change = self.block_size
                    x1_change = 0
                

            #out of bounds
            if (x1 >= self.resolution_width or x1 < 0) or (y1 >= self.resolution_height or y1 < 0):
                self.game_close = True
                self.gameLoop()
            
            #apply the modification
            x1 += x1_change
            y1 += y1_change

            self.dis.fill(self.color_dict["black"])
            pygame.draw.rect(self.dis, self.color_dict["red"], [foodx, foody, self.block_size, self.block_size])
            
            #Account for the head, which is the decision point
            self.snake_Head = []
            self.snake_Head.append(x1)
            self.snake_Head.append(y1)
            self.snake_Body.append(self.snake_Head)
            
            if len(self.snake_Body) > snake_length:
                del self.snake_Body[0]
            # SELF-CRASH: Last entry (:-1) is the head position. If a segment's coordinates match the head's coordinates, Game Over.
            for x in self.snake_Body[:-1]:
                if x == self.snake_Head:
                    self.game_close = True
            self.snake_plotter()
            #self.score_generator(snake_length - 1)
            pygame.display.update()
            if x1 == foodx and y1 == foody:
                foodx, foody = self.food_generator()  # We generate the next food before updating the screen.
                pygame.draw.rect(self.dis, self.color_dict["red"], [foodx, foody, self.block_size, self.block_size])
                pygame.display.update()
                snake_length += 1
            self.final_speed = self.snake_speed+speed_mod
            self.clock.tick(self.final_speed)
            self.cycle += 1
            #pygame.image.save(self.dis,"screenshot.png")
    
        pygame.quit()
        quit()



def main():
    snek = SnakeGame()
    snek.gameLoop()

if __name__ == "__main__":
    main()