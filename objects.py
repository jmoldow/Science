import pygame

__all__ = ['GameObject', 'Stalactite', 'Platform', 'Stalagmite', 'Character']

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

    def getGlobalMapPosition(self):
        return self.getPosition()

    def getRelativeWindowPosition(self, visible_window_tl = [0,0]):
        return [self._position[i] - visible_window_tl[i] for i in range(2)]
    
    def setPosition(self, position):
        self._position = position

    def setRelativeWindowPosition(self, position, visible_window_tl = [0,0]):
        self.setPosition([position[i] + visible_window_tl[i] for i in range(2)])

    def logic(self):
        pass

    def render(self, window, visible_window_tl):
        if self._imagename:
            window.blit(pygame.image.load(self.getImageName()), self.getRelativeWindowPosition(visible_window_tl))

class Stalactite(GameObject):
    _map_char = 'V'
    _imagename = 'media/images/stalactite.png'

class Platform(GameObject):
    _map_char = '-'
    _imagename = 'media/images/platform.png'

class Stalagmite(GameObject):
    _map_char = '^'
    _imagename = 'media/images/stalagmite.png'

class Character(GameObject):
    _map_char = 'C'
    _imagename = 'media/images/etymology_man.png'
