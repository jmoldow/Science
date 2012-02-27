import pygame
from pygame.locals import *

__all__ = ['ScienceSprite', 'StalactiteSprite', 'PlatformSprite', 'StalagmiteSprite', 'CharacterSprite']

# TODO - we shouldn't have to reproduce this in both files
keypad_to_pixel_dir_map = {K_UP:(1,-1), K_DOWN:(1,1), K_RIGHT:(0,1), K_LEFT:(0,-1)}
dir_keys = keypad_to_pixel_dir_map.keys()
tile_size = (32, 32)

class ScienceSprite(pygame.sprite.Sprite):
    
    _imagename = ''
    _map_char = ''
    
    def __init__(self,position,*args,**kwargs):
        self._position = list(position)
        super(ScienceSprite,self).__init__(*args,**kwargs)
    
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
    
    def update(self, *args):
        kwargs = args[0]
        mapDimensions = kwargs['mapDimensions']
        tile_size = kwargs['tile_size']
        self.return_to_map(mapDimensions, tile_size)

    def render(self, window, visible_window_tl):
        if self._imagename:
            pos = self.getRelativeWindowPosition(visible_window_tl)
            window_dims = window.get_size()
            for i in range(2):
                if pos[i] + tile_size[i] < 0 or pos[i] >= window_dims[0]:
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

