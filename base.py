import pygame
import os


BASE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("img", "base.png")))

class Base:
    VELOCITY = 5
    WIDTH = BASE_IMG.get_width()

    def __init__(self,y):
        self.y = y
        # use 2 image to similate the moving base
        self.x1 = 0
        self.x2 = self.WIDTH
        self.img = BASE_IMG

    def move(self):
        # set both base moving to the left
        self.x1 -= self.VELOCITY
        self.x2 -= self.VELOCITY

        # if x1 base moved completely outside the screen
        # move it behind x2
        if self.x1 + self.WIDTH < 0:
            self.x1 = self.x2 + self.WIDTH
        # if x2 base moved completely outside the screen
        # move it behind x1
        if self.x2 + self.WIDTH < 0:
            self.x2 = self.x1 + self.WIDTH

    def animation(self, window):
        window.blit(self.img, (self.x1, self.y))
        window.blit(self.img, (self.x2, self.y))
        
