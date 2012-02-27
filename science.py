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
character_frame_size = (320,240)

windowSurfaceObj = pygame.display.set_mode(resolution)
pygame.display.set_caption('Science!')

whiteColor = pygame.Color(255,255,255)
menuImg = pygame.image.load('media/images/menu.png')
keypad_to_pixel_dir_map = {K_UP:(1,-1), K_DOWN:(1,1), K_RIGHT:(0,1), K_LEFT:(0,-1)}
dir_keys = keypad_to_pixel_dir_map.keys()

map = maps.Map(filename=mapname)
all_objects = map.load(windowSurfaceObj, tile_size)
mapDimensions = map.getDimensions()
characterObj = None
if len(all_objects['CharacterSprite']) == 1:
    characterObj = all_objects['CharacterSprite'].sprites()[0]
elif len(all_objects['CharacterSprite']):
    raise Exception('The map you loaded has more than two character starting positions.')
else:
    raise Exception('The map you loaded has no character starting position.')

def correctWindowforBoundary(visible_window_tl, resolution, tile_size, mapDimensions):
    new_visible_window_tl = list(visible_window_tl)
    for i in range(2):
        if new_visible_window_tl[i] < 0:
            new_visible_window_tl[i] = 0
        elif new_visible_window_tl[i] + resolution[i] > mapDimensions[i]*tile_size[i]:
            new_visible_window_tl[i] = mapDimensions[i]*tile_size[i] - resolution[i]
    return new_visible_window_tl

def moveWindow(characterPosition, visible_window_tl, resolution, tile_size, character_frame_size, mapDimensions):
    new_visible_window_tl = list(visible_window_tl)
    for i in range(2):
        if (characterPosition[i]+(tile_size[i]/2)-(character_frame_size[i]/2)) < visible_window_tl[i]:
            new_visible_window_tl[i] = characterPosition[i]+(tile_size[i]/2)-(character_frame_size[i]/2)
        elif (characterPosition[i]+(tile_size[i]/2)+(character_frame_size[i]/2)) > visible_window_tl[i] + resolution[i]:
            new_visible_window_tl[i] = characterPosition[i] + (tile_size[i]/2) + (character_frame_size[i]/2) - resolution[i]
    return correctWindowforBoundary(new_visible_window_tl, resolution, tile_size, mapDimensions)

def centerWindow(characterPosition, resolution, tile_size, mapDimensions):
    new_visible_window_tl = [characterPosition[i]+(tile_size[i]/2)-(resolution[i]/2) for i in range(2)]
    return correctWindowforBoundary(new_visible_window_tl, resolution, tile_size, mapDimensions)

visible_window_tl = centerWindow(characterObj.getPosition(), resolution, tile_size, mapDimensions) 

menu = True
while menu:
    windowSurfaceObj.fill(whiteColor)
    windowSurfaceObj.blit(menuImg, (0,0))
    for event in pygame.event.get():
        if event.type == MOUSEBUTTONDOWN:
            x, y = event.pos
            if 200 < y < 282:
                menu = False
            elif 355 < y < 459:
                menu = False
                pygame.quit()
                sys.exit()
    if menu:
        pygame.display.update()
        fpsClock.tick(100)

while True:
    windowSurfaceObj.fill(whiteColor)
    visible_window_tl = moveWindow(characterObj.getPosition(), visible_window_tl, resolution, tile_size, character_frame_size, mapDimensions)

    for sprite_name, sprite_group in all_objects.iteritems():
        sprite_group.update({'mapDimensions':mapDimensions,'tile_size':tile_size})
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    
    for object_type in objects.__all__:
        for gameObj in all_objects[object_type]:
            gameObj.render(windowSurfaceObj, visible_window_tl)
    
    pygame.display.update()
    fpsClock.tick(100)


