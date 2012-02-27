import objects
from collections import defaultdict
import pygame

class Map(object):

    def __init__(self, filename=None):
        f = open(filename, 'r')
        self._data = f.readlines()
        for i in range(len(self._data)):
            self._data[i] = self._data[i][:-1]
        self._dimensions = (len(self._data[0]), len(self._data))
        f.close()

    def getWidth(self):
        return self._dimensions[0]

    def getHeight(self):
        return self._dimensions[1]

    def getDimensions(self):
        return self._dimensions

    def get_terrain_type(self, position):
        # Position is a tuple (col, row)
        col, row = position
        char = self._data[row][col]
        for object_type_name in objects.__all__:
            object_type = getattr(objects, object_type_name, None)
            if object_type is None:
                raise Exception("You should update objects.__all__")
            if char == object_type.getMapChar():
                return object_type
        return None

    def load(self, window, tile_size):
        width, height = tile_size
        all_objects = defaultdict(pygame.sprite.Group)
        for i in range(self.getWidth()):
            for j in range(self.getHeight()):
                terrain_type = self.get_terrain_type((i,j))
                if terrain_type is not None:
                    gameObj = terrain_type((i*width, j*height))
                    all_objects[gameObj.__class__.__name__].add(gameObj)
        return all_objects
