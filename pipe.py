import pygame
import os
import random

PIPE_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("img", "pipe.png")))

class Pipe:
    GAP = 200    # gap between top and bottom pipes
    VELOCITY = 5 # velocity at which pipes are moving

    def __init__(self, x):
        self.x = x
        self.height = 0
        self.top = 0    # top pipe position in y
        self.bottom = 0 # bottom pipe postion in y
        # This is the top pipe horizontal flip = False vertical flip = True
        self.top_pipe = pygame.transform.flip(PIPE_IMG, False, True)
        self.bottom_pipe = PIPE_IMG

        self.passed = False
        self.set_height()

    def set_height(self):
        self.height = random.randrange(50,450)
        # all images are drawn from its topleft corner 
        self.top = self.height - self.top_pipe.get_height() # get_height() get the image height
        self.bottom = self.height + self.GAP

    def move(self):
        self.x -= self.VELOCITY

    def animation(self,window):
        window.blit(self.top_pipe, (self.x, self.top))
        window.blit(self.bottom_pipe, (self.x, self.bottom))

    def collision(self, bird):
        bird_mask = bird.get_mask()
        top_mask = pygame.mask.from_surface(self.top_pipe)
        bottom_mask = pygame.mask.from_surface(self.bottom_pipe)

        # The offset calculate the coordinate between 2 surfaces according to their topleft corner
        top_offset = (self.x - bird.x, self.top - round(bird.y))       # it can only handle integer so round 
        bottom_offset = (self.x - bird.x, self.bottom - round(bird.y))

        #overlap() find overlap in the offset area
        top_collide = bird_mask.overlap(top_mask, top_offset)
        bottom_collide = bird_mask.overlap(bottom_mask, bottom_offset)  # return None if not collide

        if top_collide or bottom_collide:
            return True

        return False


