import sys, os
import pygame
from pygame.locals import *
import maps
import objects
# from optpartse import OptionParser

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sound disabled'

# parser = OptionParser()
# parser.add_option("-f", "--filename", type="string")


assert "--file=" in sys.argv[1], "Call this program as python science.py --filename=<filename>"
mapname = sys.argv[1][7:]

pygame.init()
fpsClock = pygame.time.Clock()

resolution = (640,480)

windowSurfaceObj = pygame.display.set_mode(resolution)
pygame.display.set_caption('Science!')

characterObj = pygame.image.load('media/images/etymology_man.png')
redColor = pygame.Color(255,0,0)
greenColor = pygame.Color(0,255,0)
blueColor = pygame.Color(0,0,255)
whiteColor = pygame.Color(255,255,255)
mousex, mousey = 0, 0


map = maps.Map(filename=mapname)

while True:
    windowSurfaceObj.fill(whiteColor)
    map.render(windowSurfaceObj)

    windowSurfaceObj.blit(characterObj, (mousex, mousey))

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEMOTION:
            mousex, mousey = event.pos

    pygame.display.update()
    fpsClock.tick(30)


