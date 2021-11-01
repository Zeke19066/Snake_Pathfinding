import pygame
screen_width, screen_height = 20, 20

scaling_factor = 6

x, y = 10, 10
rect_width, rect_height = 2, 2
vel = 2
black = (0, 0, 0)
white = (255, 255, 255)
pygame.init()
win = pygame.display.set_mode((screen_width*scaling_factor, screen_height*scaling_factor))

screen = pygame.Surface((screen_width, screen_height))

run = True
while run:
    pygame.time.delay(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    screen.fill(black)
    pygame.draw.rect(screen, white, (x, y, rect_width, rect_height))

    win.blit(pygame.transform.scale(screen, win.get_rect().size), (0, 0))
    pygame.display.update()
pygame.quit()