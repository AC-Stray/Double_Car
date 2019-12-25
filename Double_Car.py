import pygame, sys, time
from pygame.locals import *

pygame.init()

screen = pygame.display.set_mode((480, 350))
screen.fill((255, 255, 255))
pygame.display.set_caption("Double Car")
car1 = pygame.image.load("Red.png")
car2 = pygame.image.load("Yellow.png")
bg = pygame.image.load("Racetrack.png")
            
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        sys.exit()

    screen.blit(bg, (0, 0))
    
    pygame.display.update()
