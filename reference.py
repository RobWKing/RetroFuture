# 31st may goals: set gameover function when hit, save score to high score, level 2 and 3 backgrounds

# make ship fire down as well as up
# multiple enemies  (a real pain with my spaghetti code)
# enemies can fire too?
# high score saving
# player_die()
# invader_die()
# learn how to encrypt text file for high score
# if enemies collide with each other, ping off

# --completed--
# !!! need to make it so second bullet cannot be fired until first bullet is back into a ready state
# something like when bullet reaches xyz of the Y axis, set bullet to ready mode, delete the bullet etc
# only then accept another input from P to fire another bullet

import pygame, random, time, threading
from pygame import mixer

# line49 to change enemy variable acceleration, or to combine with INVADER_SPEED for easy adjustability
# initialises pygame library
pygame.init()

screenwidth = 800
screenheight = 600
screen = pygame.display.set_mode((screenwidth, screenheight))  # create screen, set width x height
first_time = 2
second_time = 2
third_time = 0
loop_break = False
# score
current_score = 0
font = pygame.font.SysFont('consolas',20)
textX = 10
textY = 10


# icon
pygame.display.set_caption("Space Invaders")
icon = pygame.image.load('SpaceInvader.ico')
pygame.display.set_icon(icon)

# player
playerImg = pygame.image.load('shipsmall.png')
ship_width = playerImg.get_width()
ship_height = playerImg.get_height()
playerX = ((screenwidth / 2) - (ship_width / 2))
playerY = ((screenheight / 2 + (ship_height / 2)) * 1.6)  # a bit arbitrary, may make for awkward maths later?
playerX_change = 0
playerY_change = 0
SPEED = 0.75

# basic enemy
invaderImg = pygame.image.load('invadersmall.png')
invader_width = invaderImg.get_width()
invader_height = invaderImg.get_height()
invaderX = random.uniform(screenwidth * 0.25, screenwidth * 0.75)  # random for now
invaderY = random.uniform(screenheight * 0.1, screenheight * .5)
invaderX_change = 0
invaderY_change = 0
# invader_speed_low = -0.3
# invader_speed_high = 0.3
INVADER_SPEED = 0.3  # could tie this to difficulty, currently only used for reacting to hitting boundaries

invader2Img = pygame.image.load('invadersmall.png')
invader2X = random.uniform(screenwidth * 0.25, screenwidth * 0.75)  # random for now
invader2Y = random.uniform(screenheight * 0.1, screenheight * .5)
invader2X_change = 0
invader2Y_change = 0

invader3Img = pygame.image.load('invadersmall.png')
invader3X = random.uniform(screenwidth * 0.25, screenwidth * 0.75)  # random for now
invader3Y = random.uniform(screenheight * 0.1, screenheight * .5)
invader3X_change = 0
invader3Y_change = 0

# player bullet
bulletImg = pygame.image.load('bullet.png')
bullet_width = bulletImg.get_width()
bullet_height = bulletImg.get_height()
bulletY = 1
bulletX = 0
bulletY_change = 0
BULLET_SPEED = 1.5
bullet_state = "ready"  # ready = not fired, active = is drawn on screen

# background
BgImg = pygame.image.load('invaderbg.png')

# BGM [temporary]
mixer.music.load('th06_10.wav')
mixer.music.set_volume(0.5)
mixer.music.play(-1)
def show_score(x,y):
    score = font.render('Score: ' + str(current_score),True,(255,255,255))
    screen.blit(score,(x,y))
def player(x, y):
    screen.blit(playerImg, (x, y))  # means to draw on screen


def invader(x, y):
    global invaderX_change, invaderY_change, invader2Y, invader2X, invader2X_change, invader2Y_change, invader_speed_low, invader_speed_high
    global invader3Y, invader3X, invader3X_change, invader3Y_change
    global invaderX, invaderY
    global first_time, second_time, third_time

    screen.blit(invaderImg, (x, y))
    if second_time / 500 == first_time:
        invaderX_change = random.uniform(-INVADER_SPEED, INVADER_SPEED)
        # random.choice([0.2, -0.2])  if want uniform speed, or with INVADER_SPEED for easily changable difficulty
        invaderY_change = random.uniform(-INVADER_SPEED, INVADER_SPEED)
        invader2X_change = random.uniform(-INVADER_SPEED, INVADER_SPEED)
        invader2Y_change = random.uniform(-INVADER_SPEED, INVADER_SPEED)
        invader3X_change = random.uniform(-INVADER_SPEED, INVADER_SPEED)
        invader3Y_change = random.uniform(-INVADER_SPEED, INVADER_SPEED)
        invaderX += invaderX_change
        invaderY += invaderY_change
        invader2X += invader2X_change
        invader2Y += invader2Y_change
        invader3X += invader3X_change
        invader3Y += invader3Y_change
        third_time += second_time
        second_time = 2
        print(third_time)
    else:
        second_time += 1
        # print(first_time, "|", second_time)  # only for debugging


def fire_bullet_UP(x, y):
    global bullet_state, bulletX, bulletY, bulletY_change, bullet_height, bullet_width, ship_width, bulletImg, bulletY_2
    bullet_state = "fire"
    # bulletY = x + (ship_width/2 - bullet_width/2)
    # bulletX = (playerY - 15)
    if bulletY >= -bullet_height:  # makes it move upwards, to Y-axis 0 - bullet height so it fully disappears
        bulletY -= BULLET_SPEED
    screen.blit(bulletImg, (bulletX, bulletY))
    # print(f"bullet state: {bullet_state}")
    # if bulletY <= -bullet_height:
    # bullet_state = "ready"
    # screen.blit(bulletImg, (x + (ship_width/2 - bullet_width/2), y - 15))  # not sure on this maths
    # bulletY_change = -1


def fire_bullet_DOWN(x, y):
    pass


# this loop keeps the game running indefinitely until pygame.QUIT is called (pressing x)
# if you want something consistent to be running at all times, put inside the loop
running = True  # set a loop to keep window open, can shut by setting running = False later on
while running:
    screen.blit(BgImg, (0, 0))
    for event in pygame.event.get():  # this will check for all events in the whole program, arrow presses, buttons etc
        if event.type == pygame.QUIT:
            running = False
        # all of the inputs have an issue with overlap, where pressing other directions too fast causes missed inputs, investigate GPTs code to see why their's doesnt
        if event.type == pygame.KEYDOWN:  # pressing any button on keyboard = KEYDOWN, KEYUP = releasing
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                print('left')
                playerX_change = -SPEED
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                print('right')
                playerX_change = SPEED
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT or event.key == pygame.K_d or event.key == pygame.K_a:  # this prevents a 'key released' by releasing other non-mapped keys
                print('X key released')
                playerX_change = 0
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN or event.key == pygame.K_w or event.key == pygame.K_s:
                print('Y key released')
                playerY_change = 0
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                print('up')
                playerY_change = -SPEED
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_DOWN or event.key == pygame.K_s:
                print('down')
                playerY_change = SPEED

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p and bullet_state == "ready":  # makes it so can only fire one bullet at a time
                print('shoot up')
                bullet_sound = mixer.Sound('LASER.WAV')
                bullet_sound.play()
                bulletX = playerX + (ship_width / 2 - bullet_width / 2)
                bulletY = (playerY - 12)
                if bullet_state == "ready":
                    fire_bullet_UP(bulletX, bulletY)
                else:
                    pass
    # check for keystrokes and update player coordinates

    # screen.fill((255, 255, 255))  # RGB colours, need to first draw screen fill, then draw other things, obviously, not needed now
    playerX += playerX_change  # add or minus direction to playerX
    playerY += playerY_change
    if playerX <= 0:  # stops it exceeding the boundaries of the screen
        playerX = 0
    elif playerX >= (screenwidth - ship_width):
        playerX = screenwidth - ship_width
    if playerY <= 0:
        playerY = 0
    elif playerY >= (screenheight - ship_height):
        playerY = screenheight - ship_height

    if invaderX <= 0:
        invaderX = 0
        invaderX_change += INVADER_SPEED
    elif invaderX >= (screenwidth - invader_width):
        invaderX = screenwidth - invader_width
        invaderX_change -= INVADER_SPEED
    if invaderY <= 0:  # !!! stop invader going below y-axis 0, need to change to be a higher value, but not sure how to yet
        invaderY = 0
        invaderY_change += INVADER_SPEED
    elif invaderY >= (screenheight - invader_height):
        invaderY = screenheight - invader_height
        invaderY_change -= INVADER_SPEED

    if invader2X <= 0:
        invader2X = 0
        invader2X_change += INVADER_SPEED
    elif invader2X >= (screenwidth - invader_width):
        invader2X = screenwidth - invader_width
        invader2X_change -= INVADER_SPEED
    if invader2Y <= 0:  # !!! stop invader going below y-axis 0, need to change to be a higher value, but not sure how to yet
        invader2Y = 0
        invader2Y_change += INVADER_SPEED
    elif invader2Y >= (screenheight - invader_height):
        invader2Y = screenheight - invader_height
        invader2Y_change -= INVADER_SPEED

    if invader3X <= 0:
        invader3X = 0
        invader3X_change += INVADER_SPEED
    elif invader3X >= (screenwidth - invader_width):
        invader3X = screenwidth - invader_width
        invader3X_change -= INVADER_SPEED
    if invader3Y <= 0:  # !!! stop invader going below y-axis 0, need to change to be a higher value, but not sure how to yet
        invader3Y = 0
        invader3Y_change += INVADER_SPEED
    elif invader3Y >= (screenheight - invader_height):
        invader3Y = screenheight - invader_height
        invader3Y_change -= INVADER_SPEED

    # ---bullet movement---
    if bullet_state == "fire":
        fire_bullet_UP(bulletX, bulletY)
    if bulletY < 0:  # when bullet reaches end of screen...
        bullet_state = "ready"  # set bullet status back to ready
        # bulletY = (playerY - 12)  # and reset the bullet's Y-axis to in front of the ship for when it's next fired !! this code does nothing
    # print(bullet_state)  # for debug

    # ---check for bullet on enemy collision---
    if invaderImg.get_rect(x=invaderX, y=invaderY).colliderect(bulletImg.get_rect(x=bulletX, y=bulletY)):
        print("hit")
        invader_shot = mixer.Sound('boom.wav')
        invader_shot.play()
        bulletY = (playerY - 12)
        bullet_state = "ready"
        current_score += 1
        print(current_score)

    # ---check for bullet on enemy 2 collision---
    if invader2Img.get_rect(x=invader2X, y=invader2Y).colliderect(bulletImg.get_rect(x=bulletX, y=bulletY)):
        print("hit")
        bulletY = (playerY - 12)
        invader_shot = mixer.Sound('boom.wav')
        invader_shot.play()
        bullet_state = "ready"
        current_score += 1
        print(current_score)

    # ---check for bullet on enemy 3 collision---
    if invader3Img.get_rect(x=invader3X, y=invader3Y).colliderect(bulletImg.get_rect(x=bulletX, y=bulletY)):
        print("hit")
        bulletY = (playerY - 12)
        invader_shot = mixer.Sound('boom.wav')
        invader_shot.play()
        bullet_state = "ready"
        current_score += 1
        print(current_score)

    # ---check for enemy ship on player collision---
    if invaderImg.get_rect(x=invaderX, y=invaderY).colliderect(playerImg.get_rect(x=playerX, y=playerY)):
        print("enemy ship collided with player")
        invader_shot = mixer.Sound('boom.wav')   # makes it very laggy bc of repeated collisions, but np because later game will end at this point
        invader_shot.play()  # temporary
        #player_die()

    # ---check for enemy 2 ship on player collision---
    if invader2Img.get_rect(x=invader2X, y=invader2Y).colliderect(playerImg.get_rect(x=playerX, y=playerY)):
        print("enemy ship 2 collided with player")
        invader_shot = mixer.Sound('boom.wav')
        invader_shot.play()  # temporary
        #player_die()

    # ---check for enemy 3 ship on player collision---
    if invader3Img.get_rect(x=invader3X, y=invader3Y).colliderect(playerImg.get_rect(x=playerX, y=playerY)):
        print("enemy ship 2 collided with player")
        invader_shot = mixer.Sound('boom.wav')
        invader_shot.play()  # temporary
        #player_die()

    #---check for enemy bullet on player collision PLACEHOLDER---
    if 9 > current_score > 3 and loop_break is False:
        BgImg = pygame.image.load('invaderbg2.png')
        # invader_speed_low = -0.5  # leads to getting stuck on edges, need to change INVADER_SPEED also probably fixes it
        # invader_speed_high = 0.5
        INVADER_SPEED = 0.5
        loop_break = True
    if current_score > 9:
        # invader_speed_low = -0.75
        # invader_speed_high = 0.75
        INVADER_SPEED = 0.75


    player(playerX, playerY)
    invaderX += invaderX_change
    invaderY += invaderY_change
    invader2X += invader2X_change
    invader2Y += invader2Y_change
    invader3X += invader3X_change
    invader3Y += invader3Y_change
    invader(invaderX, invaderY)
    invader(invader2X,invader2Y)
    invader(invader3X,invader3Y)
    show_score(textX,textY)
    pygame.display.update()
