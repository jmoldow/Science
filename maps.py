import objects
from collections import defaultdict
import pygame

dimensions = (0,0)
data = []
imagename = ''
imgsurf = None

def parse_map_file(filename):
    global dimensions, data, imagename, imgsurf
    f = open(filename, 'r')
    data = f.readlines()
    for i in range(len(data)):
        data[i] = data[i][:-1]
    imagename = data[0]
    if '.png' in imagename:
        imgsurf = pygame.image.load(imagename)
        data = data[1:]
    else:
        imagename = ''
    dimensions = (len(data[0]), len(data))
    f.close()

def get_terrain_type(position):
    # Position is a tuple (col, row)
    col, row = position
    char = data[row][col]
    for object_type_name in objects.__all__:
        object_type = getattr(objects, object_type_name, None)
        if object_type is None:
            raise Exception("You should update objects.__all__")
        if char == object_type.getMapChar():
            return object_type
    return None

def load(window):
    all_objects = defaultdict(pygame.sprite.Group)
    for i in range(dimensions[0]):
        for j in range(dimensions[1]):
            terrain_type = get_terrain_type((i,j))
            if terrain_type is not None:
                terrain_type(position=(i,j),groups=[all_objects[terrain_type.__name__]])
    return all_objects
