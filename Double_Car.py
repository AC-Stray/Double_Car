import pygame, sys, time, random
from pygame.locals import *
from Class_Button import button

# key description
kdc = '''
Key description:
    press key A to move the red car to racetrack 1
    press key R to move the red car to racetrack 2
    press key < to move the yellow car to racetrack 3
    press key > to move the yellow car to racetrack 4
    press key R to initialization the game (replay / start the game)
'''
print(kdc)

# ready
pygame.init()

screen = pygame.display.set_mode((600, 400))
screen.fill((255, 255, 255))
black = (0, 0, 0)
white = (255, 255, 255)
pygame.display.set_caption("Double Car by AbsoCube")
icon = pygame.image.load("racing_flag.ico")
pygame.display.set_icon(icon)
car1 = pygame.image.load("Red.png")
car2 = pygame.image.load("Yellow.png")
bg = pygame.image.load("Racetrack.png")
bg = pygame.transform.smoothscale(bg, (600, 400))
rb = pygame.image.load("RB.png")
rb = pygame.transform.smoothscale(rb, (50, 50))
bb = pygame.image.load("BB.png")
bb = pygame.transform.smoothscale(bb, (50, 50))
tfont1 = pygame.font.Font("msyh.ttc", 70)
tfont2 = pygame.font.Font("msyh.ttc", 50)
bfont = pygame.font.Font("msyh.ttc", 25)
srect = screen.get_rect()
title1 = tfont1.render('Double Car', True, black)
t1rect = title1.get_rect()
t1rect.centerx = srect.centerx
t1rect.centery = 100
title2 = tfont2.render('by AbsoCube', True, black)
t2rect = title2.get_rect()
t2rect.centerx = srect.centerx
t2rect.centery = 200
start = button(50, 270, 500, 35, "Play", bfont, (255, 0, 0), white)
RT1 = 1
RT2 = 3
point = time.time()
roadblocks = []
stop = True
over = False


def blitcar(car, rt):
    rect = car.get_rect()
    pos = rt*150-75
    rect.centerx = pos
    rect.centery = 320
    screen.blit(car, rect)


def random_roadblock():
    global roadblocks
    red = random.randint(0, 2)
    blue = random.randint(0, 2)
    colors = [[rb, red], [bb, blue]]
    totalpos = []
    for color in colors:
        oldposes = []
        for i in range(1, color[1]+1):
            while True:
                conflag = False
                pos = random.randint(1, 4)
                if pos not in oldposes and pos not in totalpos:
                    for oldpos in oldposes:
                        if pos+oldpos == 3 or pos+oldpos == 7:
                            conflag = True
                    if conflag:
                        continue
                    roadblocks.append({'color': color[0], 'dis': 0, 'rt': pos})
                    oldposes.append(pos)
                    totalpos.append(pos)
                    break


def initialization():
    global stop, RT1, RT2, point, roadblocks
    stop = False
    RT1 = 1
    RT2 = 3
    point = time.time()
    roadblocks = []
            

# main programme begin
while True:
    # handle input
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif start.pressed(event) and stop:
            initialization()
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
    elif keys[K_r]:
        initialization()

    # show background
    screen.blit(bg, (0, 0))

    if stop:
        # game's cover
        screen.blit(title1, t1rect)
        screen.blit(title2, t2rect)
        start.show(screen)

    elif not stop and not over:
        # show car(player)
        blitcar(car1, RT1)
        blitcar(car2, RT2)

        # create roadblock
        if time.time()-point >= 0.8:
            point = time.time()
            random_roadblock()

        # show & move roadblock
        for roadblock in roadblocks:
            brect = roadblock['color'].get_rect()
            brect.bottom = int(roadblock['dis'])
            brect.centerx = roadblock['rt']*150-75
            screen.blit(roadblock['color'], brect)
            roadblock['dis'] += 1.5

        # hit?
        ord = -1
        for roadblock in roadblocks:
            ord += 1
            crect = car1.get_rect()
            if 320+crect.height//2+25 >= roadblock['dis'] >= 320-crect.height//2+25:
                # hit red roadblock
                if roadblock['color'] == rb and roadblock['rt'] in [RT1, RT2]:
                    stop = True
            # miss & get blue roadblock
            if roadblock['color'] == bb:
                if roadblock['rt'] not in [RT1, RT2] and 320+crect.height//2 <= roadblock['dis']:
                    stop = True
                elif 320+crect.height//2-25 >= roadblock['dis'] >= 320-crect.height//2+25:
                    if roadblock['rt'] in [RT1, RT2]:
                        del roadblocks[ord]
                        ord -= 1
            # touch edge & get roadblock
            if roadblock['dis'] >= 450:
                del roadblocks[ord]
                ord -= 1
    pygame.display.update()
