from PIL import Image
import os
import cv2
import numpy as np


class Capture():
    def __init__(self):
        print(os.getcwd())
        self.parent_dir = r"Demo"
        os.chdir(self.parent_dir)
        self.game_count = 0
        self.gif_stack = []

    def snap_maker(self, img):
        PIL_image = Image.fromarray(np.uint8(img)).convert('RGB')
        self.gif_stack.append(PIL_image)

    def gif_maker(self):
        self.game_count += 1
        self.gif_stack[0].save(f'{self.game_count}out.gif', save_all=True, append_images=self.gif_stack[1:], optimize=True, duration=100, loop=0)
        self.gif_stack = []

def main():
    capt = Capture()


if __name__ == "__main__":
    main()


"""
#To generate frame in pygame:

frame = pygame.surfarray.array3d(self.dis)
self.gif.snap_maker(frame)

"""