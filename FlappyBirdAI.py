import pygame
import neat
import time
import os
import random

# import bird class from bird.py
from bird import Bird
from pipe import Pipe
from base import Base

# set window dimension
WIN_WIDTH = 500
WIN_HEIGHT = 800
# initialize window and bird
window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
bird = Bird(130,300)
pipes = [Pipe(WIN_WIDTH)]
base = Base(WIN_HEIGHT - 50)
# setting for FPS
clock = pygame.time.Clock()
# loading background image
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("img", "bg.png")))
pygame.font.init()
FONT = pygame.font.SysFont("comicsans", 50)

def display(window, bird, pipe, base, score):
    # This displat layer by layer
    window.blit(BG_IMG, (0,0)) #blit is draw
    bird.animation(window)

    # display pipes
    for pipe in pipes:
        pipe.animation(window)
    
    # display base
    base.animation(window)

    # display score
    text = FONT.render("score: " + str(score), 1, (255,255,255))
    window.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))

    pygame.display.update()

    

# main game loop. This loop runs 30 times per second
while True:
    # set FPS to 30
    clock.tick(30)
    # set score
    score = 0
    # move objects
    base.move()
    #bird.move()
    #move pipe
    add_pipe = False
    # list of pipe moved out of screen
    remove = []
    # pipes is a list, iterate them in for loop 
    for pipe in pipes:
        if pipe.collision(bird):
            pass

        # if the pipe move off the screen add it to the remove list
        if pipe.x + pipe.top_pipe.get_width() < 0:
            remove.append(pipe)
        
        # if bird passed pipe, set pipe pass = True and add a pipe
        if not pipe.passed and pipe.x < bird.x:
            pipe.passed = True
            add_pipe = True
            
        pipe.move()
    
    # adding pipes
    if add_pipe:
        score += 1
        pipes.append(Pipe(WIN_WIDTH))
    # removing passed pipes
    for r in remove:
        pipes.remove(r)

    # Failure condition: collide with groud
    if bird.y + bird.img.get_height() >= 750:
        pass

    #display window
    display(window, bird, pipes, base, score)

    # check user input
    for event in pygame.event.get():

        # click topright X
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    
    

