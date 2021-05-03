import pygame
import neat
import time
import os
import random
from pygame import mixer

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
# set score
score = 0
# setting for FPS
clock = pygame.time.Clock()
# load background image
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("img", "bg.png")))
pygame.font.init()
FONT = pygame.font.SysFont("Agency FB", 50, True)
# load sound
mixer.init()
wing_sound = mixer.Sound("Wing.mp3")
mixer.Sound.set_volume(wing_sound, 0.1)
score_sound = mixer.Sound("Score.mp3")
mixer.Sound.set_volume(score_sound, 0.1)
die_sound = mixer.Sound("Die.mp3")
mixer.Sound.set_volume(die_sound, 0.1)
collision_sound = mixer.Sound("Collision.mp3")
mixer.Sound.set_volume(collision_sound, 0.1)

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
    text = FONT.render(str(score),1 ,(255,255,255))
    window.blit(text, (250 - text.get_width()/2,150))

    pygame.display.update()

    

# main game loop. This loop runs 30 times per second
while True:
    # set FPS to 30
    clock.tick(30)
    # move objects
    base.move()
    bird.move()
    #move pipe
    add_pipe = False
    # list of pipe moved out of screen
    remove = []
    # pipes is a list, iterate them in for loop 
    for pipe in pipes:
        if pipe.collision(bird):
            collision_sound.play()
            die_sound.play()

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
        score_sound.play()

    # removing passed pipes 
    for r in remove:
        pipes.remove(r)

    # Failure condition
    if bird.y + bird.img.get_height() >= 750:
        pass

    #display window
    display(window, bird, pipes, base,score)

    # check user input
    for event in pygame.event.get():

        # click topright X
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.jump()
                wing_sound.play()
    
    

