import pygame
import os
# transform.scale2x makes images 2x bigger
# os.path.join("folder name", "file name")
BIRD_IMGS = [pygame.transform.scale2x(pygame.image.load(os.path.join("img", "bird1.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("img", "bird2.png"))),
             pygame.transform.scale2x(pygame.image.load(os.path.join("img", "bird3.png")))]

class Bird:
    IMGS = BIRD_IMGS
    ANIMATION_TIME = 5
    MAX_ROTATION = 25  # how much bird tilt
    ROT_VEL = 15       # rotation velocity originally 20
    
    def __init__(self, x, y):
        # starting postion of bird
        self.x = x
        self.y = y
        self.tilt = 0
        self.tick_count = 0
        self.vel = 0
        self.height = self.y
        self.img_count = 0       # counting which image we have so we can animate it
        self.img = self.IMGS[0]  # initialize first image of the bird

    # when press "space bar" call this
    def jump(self):
        # pygame initialize window (0,0) at top left corner
        # going up requires negative velocity
        # lef/right movement is the same
        self.vel = -9      # originally -10.5
        self.tick_count = 0
        self.height = self.y
    
    # call everytime the main game loop runs
    def move(self):
        # we call every frame to move bird
        self.tick_count += 1    # tick_count +1 for every frame

        # how many pixels we move each frame
        # For example: one frame after jump is called
        # -10.5 * 1 + 1.5 * 1^2 = -9
        # the 1.5*self.tick_count**2 is like gravity
        # distance travel = g*t^2 = 1.5 * tick_count^2
        displacement = self.vel*self.tick_count + 1.2*self.tick_count**2    # originally 1.5
        
        # terminal velocity: max velocity going downward
        if displacement >= 16:
            displacement = 16
        # fine tune the movement. TEST THIS!
        if displacement < 0:
            displacement -= 3
        
        # setting y coordinate
        self.y = self.y + displacement

        # tilting the bird
        # tile up when going up
        if displacement < 0 :
            # since every time the bird jump, jump function mark the jumped position
            # if we are moving up or above the jumped position we tilt up
            if self.tilt < self.MAX_ROTATION:
                self.tilt = self.MAX_ROTATION

        # tile up when going up
        else:
            # 2 methods to 
            """
            self.tilt = self.tilt - 5*self.tick_count
            if self.tilt < -90:
                self.tilt = -90"""
            
            if self.tilt > -90:
                self.tilt -= self.ROT_VEL
            if self.tilt < -90:
                self.tilt = -90

    # since we are calling draw ing main game loop which runs 30fps
    # this will count what iteration of image our animation needs
    # animate the image every 5 frames change V2 8:31
    def animation(self, window):
        self.img_count += 1
        if self.img_count < 10:
            self.img = self.IMGS[0]
        elif self.img_count < self.ANIMATION_TIME*2:
            self.img = self.IMGS[1]
        elif self.img_count < self.ANIMATION_TIME*3:
            self.img = self.IMGS[2]
        elif self.img_count < self.ANIMATION_TIME*4:
            self.img = self.IMGS[1]
        else:
            self.img = self.IMGS[0]
            self.img_count = 0

        if self.tilt < -80:
            self.img = self.IMGS[1]

        # this is how we rotate the bird
        rotated_image = pygame.transform.rotate(self.img, self.tilt)
        # but it rotate the top left corner of the image so we need to fix it
        # found on stackoverflow
        new_rect = rotated_image.get_rect(center = self.img.get_rect(topleft = (self.x, self.y)).center)

        window.blit(rotated_image, new_rect.topleft)

    # collision
    # mask find pixels in the image and determine the collision with respect to pixel not hitbox
    def get_mask(self):
        return pygame.mask.from_surface(self.img)
        



        

