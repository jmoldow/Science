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
mapname = sys.argv[1].partition("=")[2]

pygame.init()
fpsClock = pygame.time.Clock()

resolution = (640,480)
tile_size = (32, 32)

windowSurfaceObj = pygame.display.set_mode(resolution)
pygame.display.set_caption('Science!')

characterObj = pygame.image.load('media/images/etymology_man.png')
mousex, mousey = 0, 0
whiteColor = pygame.Color(255,255,255)


map = maps.Map(filename=mapname)
all_objects = map.load(windowSurfaceObj, tile_size)

while True:
    windowSurfaceObj.fill(whiteColor)
    
    windowSurfaceObj.blit(characterObj, (mousex, mousey))
    
    for object_type in objects.__all__:
        for gameObj in all_objects[object_type]:
            gameObj.logic()

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == MOUSEMOTION:
            mousex, mousey = event.pos

    for object_type in objects.__all__:
        for gameObj in all_objects[object_type]:
            gameObj.render(windowSurfaceObj)

    pygame.display.update()
    fpsClock.tick(30)


