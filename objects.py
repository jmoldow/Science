import pygame
import physics
from pygame.locals import *
import maps

__all__ = ['ScienceSprite', 'StalactiteSprite', 'PlatformSprite', 'BackgroundPlatformSprite', 'FireSprite', 'BeakerSprite', 'StalagmiteSprite', 'SharkSprite', 'CharacterSprite']

# TODO - we shouldn't have to reproduce this in both files
TILE_SIZE = (32, 32)
keypad_direction_map = {K_UP:(0,-1), K_RIGHT:(1,0), K_LEFT:(-1,0)}

class ScienceSprite(pygame.sprite.Sprite):
    
    _imagename = ''
    _imgsurf = None
    _map_char = ''
    _position = [0.0,0.0]
    
    def __init__(self, position, groups, size=TILE_SIZE):
        # it's possible we need a separate position variable that is a float
        self._position = list(position)
        if size == TILE_SIZE:
            self._position = [self._position[i]*TILE_SIZE[i] for i in range(2)]
        self.rectangle = pygame.Rect(self._position,size)
        if not isinstance(groups,(list,tuple)):
            groups = [groups]
        if isinstance(self._imagename,(list,tuple)):
            self._imgkey = 0
        elif isinstance(self._imagename,dict):
            self._imgkey = self._imagename.keys()[0]
        super(ScienceSprite,self).__init__(*groups)
    
    @classmethod
    def _set_imgsurf(cls):
        if cls._imagename and not cls._imgsurf:
            if isinstance(cls._imagename,basestring):
                cls._imagename = [cls._imagename]
            if isinstance(cls._imagename,(list,tuple)):
                cls._imgsurf = [pygame.image.load(name) for name in cls._imagename]
            elif isinstance(cls._imagename,dict):
                cls._imgsurf = dict([(key, pygame.image.load(cls._imagename[key])) for key in cls_imagename.keys()])
    
    def getImageName(self):
        return self._imagename[self._imgkey]
    
    def getImage(self):
        return self._imgsurf[self._imgkey]

    @property
    def image(self):
        return self.getImage()

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
        return self._position

    def getGlobalMapPosition(self):
        return self.getPosition()

    def getRelativeWindowPosition(self):
        return [self.rectangle.topleft[i] - self._visible_window_tl[i] for i in range(2)]

    def getRelativeRect(self):
        return pygame.Rect(self.getRelativeWindowPosition(),self.rectangle.size)
    
    def setPosition(self, position):
        self.rectangle.topleft = list(position)
        self._position = list(position)

    def setRelativeWindowPosition(self, position):
        self.setPosition([position[i] + self._visible_window_tl[i] for i in range(2)])

    def setRelativeRect(self, *args, **kwargs):
        new_rect = pygame.Rect(*args, **kwargs)
        self.rectangle.size = new_rect.size
        self.setRelativeWindowPosition(new_rect.topleft)
    rect = property(getRelativeRect, setRelativeRect)

    def setPositionDelta(self, delta, i=-1):
        if i==-1:
            self.rectangle.topleft = [self.rectangle.topleft[i] + delta[i] for i in range(2)]
        else:
            new_topleft = list(self.getPosition())
            new_topleft[i] += delta
            self.setPosition(new_topleft)

    def render(self, window):
        if self._imagename:
            pos = self.getRelativeWindowPosition()
            window_dims = window.get_size()
            for i in range(2):
                if pos[i] + self.rectangle.size[i] < 0 or pos[i] >= window_dims[0]:
                    return
            window.blit(self._imgsurf, pos)

class StalactiteSprite(ScienceSprite):
    _map_char = 'V'
    _imagename = 'media/images/stalactite.png'

class PlatformSprite(ScienceSprite):
    _map_char = '-'
    _imagename = 'media/images/platform.png'

class BackgroundPlatformSprite(PlatformSprite):
    _map_char = 'p'
    _imagename = ''

class FireSprite(ScienceSprite):
    _map_char = 'f'
    _imagename = 'media/images/fire.png'

class BeakerSprite(ScienceSprite):
    _map_char = '*'
    _imagename = 'media/images/beaker.png'

class StalagmiteSprite(ScienceSprite):
    _map_char = '^'
    _imagename = 'media/images/stalagmite.png'

class SharkSprite(ScienceSprite):
    _map_char = 's'
    _imagename = ['media/images/shark_left.png','media/images/shark_right.png']

    def __init__(self, position, groups, size=TILE_SIZE):
        error = True
        for delta in (-1,1):
            if 0 <= position[0]+delta < maps.dimensions[0] and maps.data[position[1]][position[0]+delta] == 'o':
                if not (0 <= position[1]-1 < maps.dimensions[1] and maps.data[position[1]-1][position[0]] == 'o' and maps.data[position[1]-1][position[0]+delta] == 'o'):
                    continue
                error = False
                position = [(position[0]+(delta-1)/2)*TILE_SIZE[0], (position[1]-1)*TILE_SIZE[1]]
                size = [2*size[i] for i in range(2)]
                super(SharkSprite,self).__init__(position=position,groups=groups,size=size)
                self._imgkey = (1-delta)/2
        if error:
            raise Exception("The shark sprite at (%s,%s) is incorrectly positioned in the map file." % (position[0],position[1]))

class CharacterSprite(ScienceSprite):
    _map_char = 'C'
    _imagename = ['media/images/character_left.png', 'media/images/DraftPlayerStill.png', 'media/images/character_right.png']
    _velocity = [0.0,0.0]

    def __init__(self, *args, **kwargs):
        self.health = 3
        self.beakers = 0
        self.invuln = 0
        super(CharacterSprite,self).__init__(*args, **kwargs)
        self._imgkey = 1

    def update(self, *args):
        if self.invuln != 0:
            self.invuln -= 1
        # gravity
        (outPos, outVel) = physics.applyConstantForce(self.getPosition(), self._velocity, (0.0,10.0), 0.1)
        self.setPosition(outPos)
        self._velocity = outVel
        
        # normal forces for collisions: todo

        forceVector = [0.0,0.0]
        for key in keypad_direction_map.keys():
            if pygame.key.get_pressed()[key]:
                forceVector[0] += 20*keypad_direction_map[key][0]
                forceVector[1] += 20*keypad_direction_map[key][1]
                
        (outPos, outVel) = physics.applyConstantForce(self.getPosition(), self._velocity, forceVector, 0.1)        
        self.setPosition(outPos)
        self._velocity = outVel
         
        # constrain position and velocity
        new_topleft = list(self.rectangle.topleft)
        for i in range(2):
            if new_topleft[i] < 0:
                new_topleft[i] = 0
                self._velocity[i] = 2
            elif new_topleft[i] > (maps.dimensions[i]-1)*self.rectangle.size[i]:
                new_topleft[i] = (maps.dimensions[i]-1)*self.rectangle.size[i]
                self._velocity[i] = -2
        self.rectangle.topleft = new_topleft

        # friction in horizontal direction of 5%
        self._velocity[0] *= 0.95

        if -1 < self._velocity[0] < 1:
            self._imgkey = 1
        elif self._velocity[0] >= 1:
            self._imgkey = 2
        elif self._velocity[0] <= -1:
            self._imgkey = 0
        super(CharacterSprite,self).update(*args)


    # STILL NEED TO HANDLE COLLISIONS
    def resolveCollision(self, collidingSprites):
        if len(collidingSprites) != 0:
            firstCollidingSprite = collidingSprites[0]
            dx = firstCollidingSprite.getPosition()[0] - self.getPosition()[0]
            dy = firstCollidingSprite.getPosition()[1] - self.getPosition()[1]
            #figure out which one is bigger
            if abs(dx) > abs(dy):
                self._velocity[0] *= -0.55
                if dx > 0:
                    self._position[0] -= 2.0
                else:
                    self._position[0] += 2.0
            else:
                self._velocity[1] *= -0.55
                if dy > 0:
                    self._position[1] -= 2.0
                else:
                    self._position[1] += 2.0


    # STILL NEED TO HANDLE COLLISIONS
    def resolveCollisionWithBeakers(self, collidingBeakers):
        for sprite in collidingBeakers:
            self.getBeaker(collidingBeakers)

    def resolveCollisionWithEvil(self, collidingEvil):
        for sprite in collidingEvil:
            if self.invuln == 0:
                self.damage()

    def getBeaker(self, collidingBeakers):
        for sprite in collidingBeakers:
            self.beakers += 1

    def damage(self):
        self.health -= 1
        self.invuln = 50

