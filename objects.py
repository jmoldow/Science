import pygame
import physics
from pygame.locals import *

__all__ = ['GameObject', 'Stalactite', 'Platform', 'Stalagmite', 'Character']

keypad_direction_map = {K_UP:(0,-1), K_RIGHT:(1,0), K_LEFT:(-1,0)}

class GameObject(object):
    
    _imagename = ''
    _map_char = ''
    
    def __init__(self,position,*args,**kwargs):
        self._position = list(position)
    
    @classmethod
    def getImageName(cls):
        return cls._imagename
    
    @classmethod
    def getMapChar(cls):
        return cls._map_char

    def getPosition(self):
        return self._position

    def getGlobalMapPosition(self):
        return self.getPosition()

    def getRelativeWindowPosition(self, visible_window_tl = [0,0]):
        return [self._position[i] - visible_window_tl[i] for i in range(2)]
    
    def setPosition(self, position):
        self._position = list(position)

    def setRelativeWindowPosition(self, position, visible_window_tl = [0,0]):
        self.setPosition([position[i] + visible_window_tl[i] for i in range(2)])
    
    def setPositionDelta(self, delta, i=-1):
        if i==-1:
            self._position = [self._position[i] + delta[i] for i in range(2)]
        else:
            self._position[i] += delta

    def return_to_map(self, mapDimensions, tile_size):
        new_position = list(self._position)
        for i in range(2):
            if new_position[i] < 0:
                new_position[i] = 0
            elif new_position[i] > (mapDimensions[i]-1)*tile_size[i]:
                new_position[i] = (mapDimensions[i]-1)*tile_size[i]
        self.setPosition(new_position)

    def logic(self,*args,**kwargs):
        pass

    def render(self, window, visible_window_tl):
        if self._imagename:
            window.blit(self._imgsurf, self.getRelativeWindowPosition(visible_window_tl))

class Stalactite(GameObject):
    _map_char = 'V'
    _imagename = 'media/images/stalactite.png'
    _imgsurf = pygame.image.load(_imagename)

class Platform(GameObject):
    _map_char = '-'
    _imagename = 'media/images/platform.png'
    _imgsurf = pygame.image.load(_imagename)    

class Stalagmite(GameObject):
    _map_char = '^'
    _imagename = 'media/images/stalagmite.png'
    _imgsurf = pygame.image.load(_imagename)
class Character(GameObject):
    _map_char = 'C'
    _imagename = 'media/images/object.png'
    _imgsurf = pygame.image.load(_imagename)
    _velocity = [0,0]

    def logic(self, mapDimensions, tile_size):
        # gravity
        physics.applyConstantForce(self, (0,10), 0.1)

        # normal forces for collisions: todo

        forceVector = [0,0]
        for key in keypad_direction_map.keys():
            if pygame.key.get_pressed()[key]:
                forceVector[0] += 20*keypad_direction_map[key][0]
                forceVector[1] += 20*keypad_direction_map[key][1]
                
        physics.applyConstantForce(self, forceVector, 0.1)        

        # constrain position and velocity
        for i in range(2):
            if self._position[i] < 0:
                self._position[i] = 0
                self._velocity[i] = 2
            elif self._position[i] > (mapDimensions[i]-1)*tile_size[i]:
                self._position[i] = (mapDimensions[i]-1)*tile_size[i]
                self._velocity[i] = -2

        # friction in horizontal direction of 5%
        self._velocity[0] *= 0.95

        # STILL NEED TO HANDLE COLLISIONS
