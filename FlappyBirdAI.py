import pygame
import neat
import time
import os
import random

# import bird class from bird.py
from bird import Bird
from pipe import Pipe
from base import Base
# loading background image
BG_IMG = pygame.transform.scale2x(pygame.image.load(os.path.join("img", "bg.png")))
pygame.font.init()
FONT = pygame.font.SysFont("Agency FB", 50, True)
# set window dimension
WIN_WIDTH = 500
WIN_HEIGHT = 800
GENERATION = 0



def display(window, birds, pipes, base, score, generation, lives):
    # This displat layer by layer
    window.blit(BG_IMG, (0,0)) #blit is draw
    for bird in birds:
        bird.animation(window)
    # display pipes
    for pipe in pipes:
        pipe.animation(window)
    
    # display base
    base.animation(window)

    # display score
    text = FONT.render("Score: " + str(score), 1, (255,255,255))
    window.blit(text, (WIN_WIDTH - 10 - text.get_width(), 10))
    text = FONT.render("Generation: " + str(generation), 1, (255,255,255))
    window.blit(text, (10, 10))
    text = FONT.render("Lives: " + str(lives), 1, (255,255,255))
    window.blit(text, (10, 60))

    pygame.display.update()



def load_config(config_path):
    config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

    pop = neat.Population(config)

    # stats reporter
    pop.add_reporter(neat.StdOutReporter(True))
    pop.add_reporter(neat.StatisticsReporter())

    winner = pop.run(main,50)   # max 50 generation  main is our fitness function


def main(genomes, config):       # fitness fuction always want genomes and config
    nets = []
    ge = []
    birds = []
    global GENERATION
    GENERATION += 1

    for _,gen in genomes:
        net = neat.nn.FeedForwardNetwork.create(gen,config)
        nets.append(net)
        birds.append(Bird(130,300))
        gen.fitness = 0    # starting score = 0
        ge.append(gen)

    # initialize window pipes and base
    window = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
    pipes = [Pipe(WIN_WIDTH)]
    base = Base(WIN_HEIGHT - 50)
    # setting for FPS
    clock = pygame.time.Clock()

    # set score
    score = 0

    # main game loop. This loop runs 30 times per second
    while True:
        # set FPS to 30
        clock.tick(30)
        # move objects
        base.move()
        # move birds
        pipe_ind = 0
        if len(birds) > 0:
            if len(pipes) > 1 and birds[0].x > pipes[0].x + pipes[0].top_pipe.get_width():  # if the bird passed the pipe
                pipe_ind = 1  # aim for the second pipe
        else:    # stop if no bird left
            break
        
        for i, bird in enumerate(birds):
            bird.move()
            ge[i].fitness += 0.1
            # 3 input that determines the output
            output = nets[i].activate((bird.y, abs(bird.y - pipes[pipe_ind].height), abs(bird.y - pipes[pipe_ind].bottom)))
            
            if output[0] > 0.5 :
                bird.jump()


        # move pipe
        add_pipe = False
        # list of pipe moved out of screen
        remove = []
        # pipes is a list, iterate them in for loop 
        for pipe in pipes:
            # we check fail or win conditions for each bird in our generation
            for i, bird in enumerate(birds):
                if pipe.collision(bird):
                    #ge[i].fitness -= 1   # punish the bird that hit the pipe by removing 1 score
                    # remove the bird that collide with pipe
                    birds.pop(i)
                    ge.pop(i)
                    nets.pop(i)

                # if bird passed pipe, set pipe pass = True and add a pipe
                if not pipe.passed and pipe.x < bird.x:
                    pipe.passed = True
                    add_pipe = True


            # if the pipe move off the screen add it to the remove list
            if pipe.x + pipe.top_pipe.get_width() < 0:
                remove.append(pipe)
                
            pipe.move()
        
        # adding pipes
        if add_pipe:
            score += 1
            # rewarding birds that made through the pipe
            for g in ge:
                g.fitness += 5 
            pipes.append(Pipe(WIN_WIDTH))

        # removing passed pipes
        for r in remove:
            pipes.remove(r)

        # Failure condition: collide with groud or sky
        for j, bird in enumerate(birds):
            if bird.y + bird.img.get_height() >= 750 or bird.y < 0 :
                # remove the bird that collide with pipe
                birds.pop(j)
                ge.pop(j)
                nets.pop(j)

        lives = len(birds)
        #display window
        display(window, birds, pipes, base, score, GENERATION, lives)

        if score > 50:
            break
        # check user input
        for event in pygame.event.get():
            # click topright X
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
    
    
if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)   # give the path we are in to load in config
    config_path = os.path.join(local_dir,"config.txt")
    load_config(config_path)
