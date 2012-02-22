import objects

class Map(object):

    def __init__(self, filename=None):
        f = open(filename, 'r')
        self._data = f.readlines()
        for line in self._data:
            line = line[:-1]
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
        return objects.GameObject

    def render(self, window):
        window_width, window_height = window.get_size()
        width_between_objects = window_width / self.getWidth()
        height_between_objects = window_height / self.getHeight()
        for i in range(self.getWidth()):
            for j in range(self.getHeight()):
                gameObj = self.get_terrain_type((i,j))()
                gameObj.render(window, (i*width_between_objects, j*height_between_objects))
