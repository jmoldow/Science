import sys, os
import pygame
from pygame.locals import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

pygame.init()
fpsClock = pygame.time.Clock()

resolution = (640,480)

windowSurfaceObj = pygame.display.set_mode(resolution)
pygame.display.set_caption('Out Dump Science Test')

drawingSurfaceObj = pygame.image.load('media/drawing.png')
redColor = pygame.Color(255,0,0)
greenColor = pygame.Color(0,255,0)
blueColor = pygame.Color(0,0,255)
whiteColor = pygame.Color(255,255,255)
mousex, mousey = 0, 0

fontObj = pygame.font.Font('freesansbold.ttf', 32)
msg = 'Hello World! This is out Science! game'

while True:
    windowSurfaceObj.fill(whiteColor)

    pygame.draw.rect(windowSurfaceObj, redColor, (10,10,50,100))

    windowSurfaceObj.blit(drawingSurfaceObj, (mousex, mousey))

    msgSurfaceObj = fontObj.render(msg, False, blueColor)
    msgRectangleObj = msgSurfaceObj.get_rect()
    msgRectangleObj.topleft = (10,20)
    windowSurfaceObj.blit(msgSurfaceObj, msgRectangleObj)


    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    pygame.display.update()
    fpsClock.tick(30)


