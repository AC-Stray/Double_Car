import pygame, sys, time, random
from pygame.locals import *

# ready
pygame.init()

screen = pygame.display.set_mode((600, 400))
screen.fill((255, 255, 255))
pygame.display.set_caption("Double Car by AbsoCube")
icon = pygame.image.load("racing_flag.ico")
pygame.display.set_icon(icon)
car1 = pygame.image.load("Red.png")
car2 = pygame.image.load("Yellow.png")
bg = pygame.image.load("Racetrack.png")
bg = pygame.transform.smoothscale(bg, (600, 400))
RT1 = 1
RT2 = 3
point = time.time()
roadblocks = []
stop = False
over = False


def blitcar(car, rt):
    rect = car.get_rect()
    pos = rt*150-75
    rect.centerx = pos
    rect.centery = 350
    screen.blit(car, rect)


def random_roadblock():
    global roadblocks
    num = random.randint(1, 4)
    rednum = num
    if rednum > 2:
        rednum = 2
    red = random.randint(0, rednum)
    blue = num-red
    colors = [['red', red], ['blue', blue]]
    oldposes = []
    for color in colors:
        for i in range(1, color[2]+1):
            while True:
                pos = random.randint(1, 4)
                if pos not in oldposes:
                    for oldpos in oldposes:
                        if pos+oldpos == 3 or pos+oldpos == 7:
                            continue
                    roadblocks.append({'color': color[0], 'dis': 0, 'rt': pos})
            

# main programme begin
while True:
    # handle input
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        sys.exit()
    elif keys[K_a]:
        RT1 = 1
    elif keys[K_d]:
        RT1 = 2
    elif keys[K_LEFT]:
        RT2 = 3
    elif keys[K_RIGHT]:
        RT2 = 4

    # show background
    screen.blit(bg, (0, 0))

    if not stop and not over:
        blitcar(car1, RT1)
        blitcar(car2, RT2)
    
    pygame.display.update()
