import time
import math, random, sys
import pygame
from pygame.locals import *

# Define some colors
BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)

RED = (255,0,0)
GREEN = (0,255,0)

BRIGHT_RED = (200,0,0)
BRIGHT_GREEN = (0,200,0)

# Define some game constants
DISPLAY_WIDTH = 800
DISPLAY_HEIGHT = 800
NARUTO_WIDTH = 100

# Load some resources
backImg = pygame.image.load('background.png')
backRect = backImg.get_rect()

narutoImg = pygame.image.load('naruto.png')
weapon1 = pygame.image.load('s1.png')
weapon2 = pygame.image.load('s2.png')
weapon3 = pygame.image.load('s3.png')
weapon4 = pygame.image.load('s4.png')
weaponList = [weapon1, weapon2, weapon3, weapon4]

# Set up game
pygame.init()
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH,DISPLAY_HEIGHT))
pygame.display.set_caption('Shuriken')

pygame.mixer.music.load('sound.wav')
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()


def textObjects(text, font, color):
    textSurface = font.render(text, True, color)
    return textSurface, textSurface.get_rect()

def messageDisplay(text, color):
    largeText = pygame.font.Font('freesansbold.ttf', 115)
    TextSurf, TextRect = textObjects(text, largeText,color)
    TextRect.center = ((DISPLAY_WIDTH / 2), (DISPLAY_HEIGHT / 2))
    gameDisplay.blit(TextSurf, TextRect)

    pygame.display.update()

    time.sleep(2)
    gameLoop()

def die():
    messageDisplay("Ouch!", RED)

def hit(weaponImg, x, y, wx, wy):
    # Check if a Shuriken hits Naruto
    narutoSurf = narutoImg.convert_alpha()
    weaponSurf = weaponImg.convert_alpha()
    naruto_mask = pygame.mask.from_surface(narutoSurf)
    weapon_mask = pygame.mask.from_surface(weaponSurf)
    offset = (int(wx - x), int(wy - y))
    return naruto_mask.overlap(weapon_mask, offset)

def button(msg,x,y,w,h,ic,ac,action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(gameDisplay, ac,(x,y,w,h))

        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, ic,(x,y,w,h))

    smallText = pygame.font.SysFont("comicsansms",20)
    textSurf, textRect = textObjects(msg, smallText, BLACK)
    textRect.center = ( (x+(w/2)), (y+(h/2)) )
    gameDisplay.blit(textSurf, textRect)


def quitGame():
    pygame.quit()
    quit()

def gameIntro():
    intro = True

    while intro:
        for event in pygame.event.get():
            #print(event)
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
        gameDisplay.fill(WHITE)
        largeText = pygame.font.SysFont("comicsansms",115)
        TextSurf, TextRect = textObjects("Shuriken", largeText, BLACK)
        TextRect.center = ((DISPLAY_WIDTH/2),(DISPLAY_HEIGHT/2))
        gameDisplay.blit(TextSurf, TextRect)

        button("GO!",150,500,100,50,GREEN,BRIGHT_GREEN,gameLoop)
        button("Quit",550,500,100,50,RED,BRIGHT_RED,quitGame)

        pygame.display.update()
        clock.tick(15)
    
def placeObject(image, x, y):
    gameDisplay.blit(image,(x,y))

def displayScore(score):
    font = pygame.font.SysFont(None, 30)
    text = font.render("SCORE: "+str(score), True, WHITE)
    gameDisplay.blit(text,(0,0))

def gameLoop():

    # Set positions for Naruto
    x = (DISPLAY_WIDTH * 0.45)
    y = (DISPLAY_HEIGHT * 0.75)

    # Will adjust Naruto's horizontal position
    x_change = 0

    # Set positions for Shuriken

    wwidth = 100
    wheight = 100
    wx = random.randrange(0, DISPLAY_WIDTH - wwidth)
    wy = -600
    wspeed = 7
    wcount = 1

    score = 0

    weapon = weaponList[random.randrange(0, 4)]
    gameExit = False

    while not gameExit:


        gameDisplay.blit(backImg, backRect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x_change = -10
                if event.key == pygame.K_RIGHT:
                    x_change = 10
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    x_change = 0

        x += x_change

        if x < 0:
            placeObject(narutoImg, 0, y)
        elif x + NARUTO_WIDTH > DISPLAY_WIDTH:
            placeObject(narutoImg, DISPLAY_WIDTH - NARUTO_WIDTH, y)
        else:
            placeObject(narutoImg, x, y)


        placeObject(weapon, wx, wy)
        displayScore(score)
        wy += wspeed
        

        if wy > DISPLAY_HEIGHT:
            wy = 0 - wheight
            wx = random.randrange(0, DISPLAY_WIDTH - wwidth)
            score += 1
            if wspeed < 30:
                wspeed += 1
            n = random.randrange(0, 4)
            weapon = weaponList[n]

        # hit(weaponImg, x, y, wx, wy)
        if hit(weapon, x, y, wx, wy):
            die()

        pygame.display.update()
        clock.tick(120)


gameIntro()
gameLoop()
pygame.quit()
quit()
