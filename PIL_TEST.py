'''
Mini play screen 100x100: (150,210) - (400,460)

screen = np.array(ImageGrab.grab(bbox=game_coords))

we need to capture a jpeg screenshot and then convert it to a numpy array for processing.
the image can be displayed by using the matplotlib plotting method below. The final image for snake game should be resized so that each block = 1 pixel.

appending the image with example.show() will also show the image.
'''

import numpy as np
from PIL import ImageGrab, Image, ImageOps
import matplotlib.pyplot as plot

#game_coords = [150, 210, 400, 460]
game_coords = [252, 251, 499, 498]

'''
# Open an exisiting file
image_path = "C:\\Users\\Ezeab\\Documents\\Python\\Snake Game\\snake_screencap.jpg"
snake_screencap_raw = Image.open(image_path)
snake_screencap_grayscale = ImageOps.grayscale(snake_screencap_raw) 
(width, height) = (10, 10)
snake_screencap = snake_screencap_grayscale.resize((width, height), resample=0)
screen = np.array(snake_screencap)
'''

#PIL.ImageGrab.grab(bbox=None, include_layered_windows=False, all_screens=False, xdisplay=None)
#generate the image from a screengrab
raw_screen = ImageGrab.grab(bbox=game_coords)
snake_screencap_grayscale = ImageOps.grayscale(raw_screen) 
(width, height) = (10, 10)
snake_screencap = snake_screencap_grayscale.resize((width, height), resample=0)
screen = np.array(snake_screencap)

#generate the image from a saved image.
print(screen)
plot.imshow(screen, cmap="gray") #use this one for greyscale.
#plot.imshow(screen)
plot.show()