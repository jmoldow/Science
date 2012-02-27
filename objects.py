import pygame
from pygame.locals import *
import maps

__all__ = ['ScienceSprite', 'StalactiteSprite', 'PlatformSprite', 'StalagmiteSprite', 'CharacterSprite']

# TODO - we shouldn't have to reproduce this in both files
keypad_to_pixel_dir_map = {K_UP:(1,-1), K_DOWN:(1,1), K_RIGHT:(0,1), K_LEFT:(0,-1)}
dir_keys = keypad_to_pixel_dir_map.keys()
TILE_SIZE = (32, 32)

class ScienceSprite(pygame.sprite.Sprite):
    
    _imagename = ''
    _map_char = ''
    
    def __init__(self,position,*groups):
        self.rect = pygame.Rect(position,TILE_SIZE)
        super(ScienceSprite,self).__init__(*groups)
    
    @classmethod
    def getImageName(cls):
        return cls._imagename
    
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
        return self.rect.topleft

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

    def return_to_map(self):
        new_position = list(self.rect.topleft)
        for i in range(2):
            if new_position[i] < 0:
                new_position[i] = 0
            elif new_position[i] > (maps.dimensions[i]-1)*self.rect.size[i]:
                new_position[i] = (maps.dimensions[i]-1)*self.rect.size[i]
        self.setPosition(new_position)
    
    def update(self, *args):
        self.return_to_map()

    def render(self, window):
        if self._imagename:
            pos = self.getRelativeWindowPosition()
            window_dims = window.get_size()
            for i in range(2):
                if pos[i] + self.rect.size[i] < 0 or pos[i] >= window_dims[0]:
                    return
            window.blit(pygame.image.load(self.getImageName()), pos)

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

    def update(self,*args):
        for KEY in dir_keys:
            if pygame.key.get_pressed()[KEY]:
                self.setPositionDelta(4*keypad_to_pixel_dir_map[KEY][1],keypad_to_pixel_dir_map[KEY][0])
        super(CharacterSprite,self).update(*args)

