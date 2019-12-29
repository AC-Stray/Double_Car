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

# read MaxScore file
with open("MaxScore.dc", "r") as maxfile:
    maxscore = maxfile.readlines()
    maxscore = maxscore[0]

# ready
pygame.init()

screen = pygame.display.set_mode((600, 400))
screen.fill((255, 255, 255))
black = (0, 0, 0)
white = (255, 255, 255)
pygame.display.set_caption("Double Car by AbsoCube --version 1.4")
icon = pygame.image.load("racing_flag.ico")
pygame.display.set_icon(icon)
car1 = pygame.image.load("Red.png")
car2 = pygame.image.load("Yellow.png")
AC = pygame.image.load("AbsoCube.jpg")
bg = pygame.image.load("Racetrack.png")
bg = pygame.transform.smoothscale(bg, (600, 400))
rb = pygame.image.load("RB.png")
rb = pygame.transform.smoothscale(rb, (50, 50))
bb = pygame.image.load("BB.png")
bb = pygame.transform.smoothscale(bb, (50, 50))
BGM = 'Adventure.mp3'
pop = 'Pop.mp3'
pygame.mixer.init(frequency=44100)
tfont1 = pygame.font.Font("msyh.ttc", 80)
tfont2 = pygame.font.Font("msyh.ttc", 50)
bfont = pygame.font.Font("msyh.ttc", 25)
sfont = pygame.font.Font("msyh.ttc", 60)
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
back = button(50, 270, 500, 35, "Back", bfont, (0, 255, 0), white)
RT1 = 1
RT1pos = 75
RT2 = 3
RT2pos = 225
point = time.time()
score = 0
roadblocks = []
effect = None
stop = True
over = False
old = False
epoint = time.time()


def blitcar(car, rtp):
    rect = car.get_rect()
    rect.centerx = rtp
    rect.centery = 320
    screen.blit(car, rect)


def random_roadblock():
    global roadblocks
    red = random.randint(0, 2)
    blue = random.randint(0, 2)
    colors = [[rb, red], [bb, blue]]
    totalpos = []
    for rbcolor in colors:
        oldposes = []
        for i in range(1, rbcolor[1]+1):
            while True:
                conflag = False
                pos = random.randint(1, 4)
                if pos not in oldposes and pos not in totalpos:
                    for oldpos in oldposes:
                        if pos+oldpos == 3 or pos+oldpos == 7:
                            conflag = True
                    if conflag:
                        continue
                    roadblocks.append({'color': rbcolor[0], 'dis': 0, 'rt': pos})
                    oldposes.append(pos)
                    totalpos.append(pos)
                    break


def initialization():
    global stop, over, RT1, RT2, point, roadblocks, score, old, effect
    pygame.mixer.music.stop()
    stop = False
    over = False
    old = True
    effect = None
    RT1 = 1
    RT2 = 3
    point = time.time()
    roadblocks = []
    score = 0
            

# show LOGO
screen.fill((255, 255, 255))
screen.blit(AC, (172, 72))
pygame.display.update()
time.sleep(3)

# main programme begin
while True:
    # handle input
    for event in pygame.event.get():
        if event.type == QUIT:
            sys.exit()
        elif start.pressed(event) and stop:
            initialization()
        elif back.pressed(event) and over:
            over = False
            stop = True
            old = False
    keys = pygame.key.get_pressed()
    if keys[K_ESCAPE]:
        sys.exit()
    if not effect:
        if keys[K_a]:
            RT1 = 1
        elif keys[K_d]:
            RT1 = 2
        if keys[K_LEFT]:
            RT2 = 3
        elif keys[K_RIGHT]:
            RT2 = 4
    if keys[K_r]:
        initialization()

    # show background
    screen.blit(bg, (0, 0))

    if stop:
        # game's cover
        screen.blit(title1, t1rect)
        screen.blit(title2, t2rect)
        start.show(screen)
        if not old:
            # game BGM
            pygame.mixer.music.stop()
            pygame.mixer.music.load(BGM)
            pygame.mixer.music.play()
            old = True

    elif not stop and not over and not effect:
        # main game logic
        # move car(player)
        if RT1*150-75 > RT1pos:
            RT1pos += 5
        elif RT1*150-75 < RT1pos:
            RT1pos -= 5
        if RT2*150-75 > RT2pos:
            RT2pos += 5
        elif RT2*150-75 < RT2pos:
            RT2pos -= 5

        # show car(player)
        blitcar(car1, RT1pos)
        blitcar(car2, RT2pos)

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
        o = -1
        for roadblock in roadblocks:
            o += 1
            crect = car1.get_rect()
            if 320+crect.height//2+25 >= roadblock['dis'] >= 320-crect.height//2+25:
                # hit red roadblock
                if roadblock['color'] == rb and roadblock['rt'] in [RT1, RT2]:
                    effect = roadblocks[o]
                    epoint = time.time()
                    del roadblocks[o]
                    o -= 1
            # miss & get blue roadblock
            if roadblock['color'] == bb:
                if roadblock['rt'] not in [RT1, RT2] and 320+crect.height//2 <= roadblock['dis']:
                    effect = roadblocks[o]
                    epoint = time.time()
                    del roadblocks[o]
                    o -= 1
                elif 320+crect.height//2-25 >= roadblock['dis'] >= 320-crect.height//2+25:
                    if roadblock['rt'] in [RT1, RT2]:
                        del roadblocks[o]
                        o -= 1
                        score += 1
                        # sound effect
                        pygame.mixer.music.load(pop)
                        pygame.mixer.music.play()
            # touch edge
            if roadblock['dis'] >= 450:
                del roadblocks[o]
                o -= 1

        # show score
        scoretext = tfont2.render(str(score), True, black)
        scorerect = scoretext.get_rect()
        scorerect.top = srect.top
        scorerect.centerx = srect.centerx
        screen.blit(scoretext, scorerect)

    elif effect:
        # death effect
        blitcar(car1, RT1pos)
        blitcar(car2, RT2pos)
        for roadblock in roadblocks:
            brect = roadblock['color'].get_rect()
            brect.bottom = int(roadblock['dis'])
            brect.centerx = roadblock['rt'] * 150 - 75
            screen.blit(roadblock['color'], brect)
        if (time.time()-epoint)//0.3 % 2 == 1:
            brect = effect['color'].get_rect()
            brect.bottom = int(effect['dis'])
            brect.centerx = effect['rt'] * 150 - 75
            screen.blit(effect['color'], brect)
        if time.time()-epoint >= 3:
            over = True
            effect = None

    elif over:
        # screen when game is over
        overtitle = sfont.render('You got '+str(score)+' scores!', True, black)
        otrect = overtitle.get_rect()
        otrect.centery = 100
        otrect.centerx = srect.centerx
        screen.blit(overtitle, otrect)
        # update max score
        with open("MaxScore.dc", "w") as maxfile:
            if score > int(maxscore):
                maxfile.write(str(score))
                maxscore = str(score)
            else:
                maxfile.write(maxscore)
        maxtext = tfont2.render('max: '+maxscore, True, black)
        mtrect = maxtext.get_rect()
        mtrect.centerx = srect.centerx
        mtrect.top = otrect.bottom
        screen.blit(maxtext, mtrect)
        back.show(screen)

    pygame.display.update()
