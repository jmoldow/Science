import pygame

__all__ = ['GameObject', 'Stalactite', 'Platform', 'Stalagmite']

class GameObject(object):
    
    _imagename = ''
    _map_char = ''
    
    def __init__(self,position,*args,**kwargs):
        self._position = position
    
    @classmethod
    def getImageName(cls):
        return cls._imagename
    
    @classmethod
    def getMapChar(cls):
        return cls._map_char
    
    def getPosition(self):
        return self._position
    
    def logic(self):
        pass

    def render(self, window):
        if self._imagename:
            window.blit(pygame.image.load(self.getImageName()), self._position)

class Stalactite(GameObject):
    _map_char = 'V'
    _imagename = 'media/images/stalactite.png'

class Platform(GameObject):
    _map_char = '-'
    _imagename = 'media/images/platform.png'

class Stalagmite(GameObject):
    _map_char = '^'
    _imagename = 'media/images/stalagmite.png'
    
