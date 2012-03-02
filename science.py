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


#assert "--file=" in sys.argv[1], "Call this program as python science.py --filename=<filename>"
#mapname = sys.argv[1].partition("=")[2]
mapname = 'maps/building.txt'

pygame.init()
fpsClock = pygame.time.Clock()

resolution = (640,480)
inventoryBarHeight = 65
windowSize = (resolution[0],resolution[1]+inventoryBarHeight)
inventoryBarImageHeight = 15
inventoryBarTextHeight = 20
character_frame_size = (320,240)

windowSurfaceObj = pygame.display.set_mode(windowSize)
pygame.display.set_caption('Science!')

whiteColor = pygame.Color(255,255,255)
blackColor = pygame.Color(0,0,0)
menuImg = pygame.image.load('media/images/menu.png')
instructionsImg = pygame.image.load('media/images/instructions.png')
keypad_to_pixel_dir_map = {K_UP:(1,-1), K_DOWN:(1,1), K_RIGHT:(0,1), K_LEFT:(0,-1)}
dir_keys = keypad_to_pixel_dir_map.keys()

heartImg = pygame.image.load('media/images/heart.png')
beakerImg = pygame.image.load('media/images/beaker.png')

for object_name in objects.__all__:
    object_type = getattr(objects,object_name,None)
    if object_type is None:
        raise Exception("You should update objects.__all__")
    else:
        object_type._set_imgsurf()

def correctWindowforBoundary(visible_window_tl):
    new_visible_window_tl = list(visible_window_tl)
    for i in range(2):
        if new_visible_window_tl[i] < 0:
            new_visible_window_tl[i] = 0
        elif new_visible_window_tl[i] + resolution[i] > maps.dimensions[i]*objects.TILE_SIZE[i]:
            new_visible_window_tl[i] = maps.dimensions[i]*objects.TILE_SIZE[i] - resolution[i]
    return new_visible_window_tl

def moveWindow(characterPosition, visible_window_tl):
    new_visible_window_tl = list(visible_window_tl)
    for i in range(2):
        if (characterPosition[i]+(objects.TILE_SIZE[i]/2)-(character_frame_size[i]/2)) < visible_window_tl[i]:
            new_visible_window_tl[i] = characterPosition[i]+(objects.TILE_SIZE[i]/2)-(character_frame_size[i]/2)
        elif (characterPosition[i]+(objects.TILE_SIZE[i]/2)+(character_frame_size[i]/2)) > visible_window_tl[i] + resolution[i]:
            new_visible_window_tl[i] = characterPosition[i] + (objects.TILE_SIZE[i]/2) + (character_frame_size[i]/2) - resolution[i]
    return correctWindowforBoundary(new_visible_window_tl)

def centerWindow(characterPosition):
    new_visible_window_tl = [characterPosition[i]+(objects.TILE_SIZE[i]/2)-(resolution[i]/2) for i in range(2)]
    return correctWindowforBoundary(new_visible_window_tl)

def playScience():
    global resolution, windowSize, inventoryBarHeight, inventoryBarImageHeight, inventoryBarTextHeight, character_frame_size, windowSurfaceObj, whiteColor
    all_objects = maps.load(windowSurfaceObj)
    all_objects['ExplosionSprite'] = pygame.sprite.Group()
    characterObj = None
    if len(all_objects['CharacterSprite']) == 1:
        characterObj = all_objects['CharacterSprite'].sprites()[0]
    elif len(all_objects['CharacterSprite']):
        raise Exception('The map you loaded has more than two character starting positions.')
    else:
        raise Exception('The map you loaded has no character starting position.')
    if len(all_objects['WinSprite']) == 0:
        raise Exception('The map you loaded has no level exit.')

    visible_window_tl = centerWindow(characterObj.getPosition())
    objects.ScienceSprite.set_visible_window_tl(visible_window_tl)

    while True:
        if characterObj.health == 0:
            windowSurfaceObj.fill(blackColor)
            font = pygame.font.Font("freesansbold.ttf", 16)
            text=font.render("You are dead.", True, whiteColor)
            textpos = text.get_rect(centerx=windowSize[0]/2)
            textpos.top = 300
            windowSurfaceObj.blit(text, textpos)
            pygame.display.update()
            pygame.time.delay(2000)
            return

        winCondition = pygame.sprite.spritecollide(characterObj, all_objects["WinSprite"], False)
        if len(winCondition) != 0:
            windowSurfaceObj.fill(blackColor)
            font = pygame.font.Font("freesansbold.ttf", 16)
            text=font.render("You escaped the lab!", True, whiteColor)
            textpos = text.get_rect(centerx=resolution[0]/2)
            textpos.top = 300
            windowSurfaceObj.blit(text, textpos)
            pygame.display.update()
            pygame.time.delay(2000)
            return

        windowSurfaceObj.fill(whiteColor)
        visible_window_tl = moveWindow(characterObj.getPosition(), visible_window_tl)
        if maps.imagename:
            windowSurfaceObj.blit(maps.imgsurf, [-coord for coord in visible_window_tl])
        objects.ScienceSprite.set_visible_window_tl(visible_window_tl)

        for sprite_name, sprite_group in all_objects.iteritems():
            sprite_group.update()
        
        collidingSprites = []
        # collidingSharks = {}
        spriteGroupsToCollideWith = [all_objects['PlatformSprite'], all_objects['BackgroundPlatformSprite']]
        for spriteGroup in spriteGroupsToCollideWith:
            collidingSprites.extend(pygame.sprite.spritecollide(characterObj, spriteGroup, False))
            # collidingSharks.update(pygame.sprite.groupcollide(all_objects['SharkSprite'], spriteGroup, False, False))
        characterObj.resolveCollision(collidingSprites)
        # for shark in collidingSharks.keys():
            # shark._velocity *= -1
            # shark._imgkey = 1-shark._imgkey

        collidingBeakers = pygame.sprite.spritecollide(characterObj, all_objects["BeakerSprite"], True)
        if len(collidingBeakers) != 0:
            characterObj.resolveCollisionWithBeakers(collidingBeakers)


        collidingEvil = []
        spriteGroupsToCollideWith = [all_objects['FireSprite'], all_objects['SharkSprite'], all_objects['StalactiteSprite'], all_objects['StalagmiteSprite']]
        for spriteGroup in spriteGroupsToCollideWith:
            collidingEvil.extend(pygame.sprite.spritecollide(characterObj, spriteGroup, False))
        if len(collidingEvil) != 0:
            characterObj.resolveCollisionWithEvil(collidingEvil)


        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN:
                if event.key == K_SPACE and characterObj.beakers > 0:
                    characterObj.beakers -= 1
                    cpos = characterObj.getPosition()
                    mypos = (cpos[0]-32, cpos[1]-32)
                    explosionSprite = objects.ExplosionSprite(mypos, all_objects['ExplosionSprite'], size=(96,96))
        # Check for shark removal
                    collidingSharkExplosions = pygame.sprite.spritecollide(explosionSprite, all_objects['SharkSprite'], True)

        if characterObj.damageFlash != 0:
            windowSurfaceObj.fill(whiteColor)
            pygame.display.update()
            fpsClock.tick(100)
            continue

        for sprite_name, sprite_group in all_objects.iteritems():
            if getattr(objects,sprite_name)._imagename:
                sprite_group.draw(windowSurfaceObj)
        # technically, this code will render every sprite, even if it is off-screen
        # at the moment, this doesn't seem to slow us down
        # if this becomes an issue, we can try something else

        
        inventory = pygame.Rect(0, resolution[1], resolution[0], inventoryBarHeight)
        windowSurfaceObj.fill(blackColor, inventory)
        windowSurfaceObj.blit(heartImg, (40,resolution[1]+inventoryBarImageHeight))
        windowSurfaceObj.blit(beakerImg, (170,resolution[1]+inventoryBarImageHeight))

        font = pygame.font.Font("freesansbold.ttf", 16)
        textHealth =font.render("x " + str(characterObj.health), True, whiteColor)
        textBeakers =font.render("x " + str(characterObj.beakers), True, whiteColor)
        windowSurfaceObj.blit(textHealth, (80,resolution[1]+inventoryBarTextHeight))
        windowSurfaceObj.blit(textBeakers, (210,resolution[1]+inventoryBarTextHeight))

        pygame.display.update()
        fpsClock.tick(100)

def instructions():
    while True:
        windowSurfaceObj.fill(whiteColor)
        windowSurfaceObj.blit(instructionsImg, (0,0))
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                if 10 < x < 85 and 20 < y < 125:
                    return
        pygame.display.update()
        fpsClock.tick(100)

if __name__ == '__main__':
    maps.parse_map_file(filename=mapname)
    while True:
        windowSurfaceObj.fill(whiteColor)
        windowSurfaceObj.blit(menuImg, (0,0))
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                x, y = event.pos
                if 200 < y < 282 and x < 515:
                    playScience()
                elif 325 < y < 450 and x < 275:
                    pygame.quit()
                    sys.exit()
                elif 310 < y < 365 and x > 345:
                    instructions()
        pygame.display.update()
        fpsClock.tick(100)
