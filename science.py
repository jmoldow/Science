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
character_frame_size = (160,160)

windowSurfaceObj = pygame.display.set_mode(resolution)
pygame.display.set_caption('Science!')

mousex, mousey = [resolution[i]/2 for i in range(2)]
whiteColor = pygame.Color(255,255,255)


map = maps.Map(filename=mapname)
all_objects = map.load(windowSurfaceObj, tile_size)
mapDimensions = map.getDimensions()
characterObj = None
if len(all_objects['Character']) == 1:
    characterObj = all_objects['Character'].pop()
    all_objects['GameObject'].append(objects.GameObject(characterObj.getPosition()))
elif len(all_objects['Character']):
    raise Exception('The map you loaded has more than two character starting positions.')
else:
    raise Exception('The map you loaded has no character starting position.')

def moveWindow(characterPosition, visible_window_tl, resolution, tile_size, character_frame_size, mapDimensions):
    new_visible_window_tl = list(visible_window_tl)
    for i in range(2):
        if (characterPosition[i]+(tile_size[i]/2)-(character_frame_size[i]/2)) < visible_window_tl[i]:
            new_visible_window_tl[i] = characterPosition[i]+(tile_size[i]/2)-(character_frame_size[i]/2)
        elif (characterPosition[i]+(tile_size[i]/2)+(character_frame_size[i]/2)) > visible_window_tl[i] + resolution[i]:
            new_visible_window_tl[i] = characterPosition[i] + (tile_size[i]/2) + (character_frame_size[i]/2) - resolution[i]
        if new_visible_window_tl[i] < 0:
            new_visible_window_tl[i] = 0
        elif new_visible_window_tl[i] + resolution[i] > mapDimensions[i]*tile_size[i]:
            new_visible_window_tl[i] = mapDimensions[i]*tile_size[i] - resolution[i]
    return new_visible_window_tl

visible_window_tl = moveWindow(characterObj.getPosition(), [0,0], resolution, tile_size, character_frame_size, mapDimensions) 

while True:
    windowSurfaceObj.fill(whiteColor)
    characterObj.setRelativeWindowPosition((mousex,mousey), visible_window_tl)
    visible_window_tl = moveWindow(characterObj.getPosition(), visible_window_tl, resolution, tile_size, character_frame_size, mapDimensions)

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
            gameObj.render(windowSurfaceObj, visible_window_tl)
    
    characterObj.render(windowSurfaceObj, visible_window_tl)

    pygame.display.update()
    fpsClock.tick(30)


