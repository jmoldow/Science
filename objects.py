import pygame
import physics
from pygame.locals import *
import maps

__all__ = ['ScienceSprite', 'StalactiteSprite', 'PlatformSprite', 'StalagmiteSprite', 'CharacterSprite']

# TODO - we shouldn't have to reproduce this in both files
TILE_SIZE = (32, 32)
keypad_direction_map = {K_UP:(0,-1), K_RIGHT:(1,0), K_LEFT:(-1,0)}

class ScienceSprite(pygame.sprite.Sprite):
    
    _imagename = ''
    _map_char = ''
    
    def __init__(self,position,*groups):
        self.rect = pygame.Rect(position,TILE_SIZE)
        super(ScienceSprite,self).__init__(*groups)
    
    @classmethod
    def _set_imgsurf(cls):
        if cls._imagename and not hasattr(cls,'_imgsurf'):
            setattr(cls,'_imgsurf',pygame.image.load(cls._imagename))
    
    @classmethod
    def getImageName(cls):
        return cls._imagename
    
    @classmethod
    def getImage(cls):
        return cls._imgsurf
    
    @classmethod
    def getMapChar(cls):
        return cls._map_char

    @classmethod
    def set_visible_window_tl(cls, visible_window_tl):
        cls._visible_window_tl = visible_window_tl

    @classmethod
    def get_visible_window_tl(cls):
        return cls._visible_window_tl

    def getPosition(self):
        return list(self.rect.topleft)

    def getGlobalMapPosition(self):
        return self.getPosition()

    def getRelativeWindowPosition(self):
        return [self.rect.topleft[i] - self._visible_window_tl[i] for i in range(2)]
    
    def setPosition(self, position):
        self.rect.topleft = list(position)

    def setRelativeWindowPosition(self, position):
        self.setPosition([position[i] + self._visible_window_tl[i] for i in range(2)])
    
    def setPositionDelta(self, delta, i=-1):
        if i==-1:
            self.rect.topleft = [self.rect.topleft[i] + delta[i] for i in range(2)]
        else:
            new_topleft = list(self.getPosition())
            new_topleft[i] += delta
            self.setPosition(new_topleft)

    def render(self, window):
        if self._imagename:
            pos = self.getRelativeWindowPosition()
            window_dims = window.get_size()
            for i in range(2):
                if pos[i] + self.rect.size[i] < 0 or pos[i] >= window_dims[0]:
                    return
            window.blit(self._imgsurf, pos)

class StalactiteSprite(ScienceSprite):
    _map_char = 'V'
    _imagename = 'media/images/stalactite.png'

class PlatformSprite(ScienceSprite):
    _map_char = '-'
    _imagename = 'media/images/platform.png'

class StalagmiteSprite(ScienceSprite):
    _map_char = '^'
    _imagename = 'media/images/stalagmite.png'

class CharacterSprite(ScienceSprite):
    _map_char = 'C'
    _imagename = 'media/images/object.png'

    _velocity = [0,0]

    def update(self, *args):
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
        new_topleft = list(self.rect.topleft)
        for i in range(2):
            if new_topleft[i] < 0:
                new_topleft[i] = 0
                self._velocity[i] = 2
            elif new_topleft[i] > (maps.dimensions[i]-1)*self.rect.size[i]:
                new_topleft[i] = (maps.dimensions[i]-1)*self.rect.size[i]
                self._velocity[i] = -2
        self.rect.topleft = new_topleft

        # friction in horizontal direction of 5%
        self._velocity[0] *= 0.95
        super(CharacterSprite,self).update(*args)

        # STILL NEED TO HANDLE COLLISIONS
