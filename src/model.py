class Vertex:
    def __init__(self, name, format, array):
        self._name = name
        self._format = format
        self._array = array

    @property
    def name(self):
        return self._name

    @property
    def format(self):
        return self._format

    @property
    def array(self):
        return self._array


class VertexLayout:
    def __init__(self):
        self.attributes = []

    def add_attribute(self, name: str, format: str, array):
        self.attributes.append(Vertex(name, format, array))

    def get_attributes(self):
        return self.attributes


class Model:
    def __init__(self, vertices=None, indices=None, colors=None, normals=None, texcoords=None):
        self.indices = indices
        self.vertex_layout = VertexLayout()

        if vertices is not None:
            self.vertex_layout.add_attribute("in_pos", "3f", vertices)
        if colors is not None:
            self.vertex_layout.add_attribute("in_color", "3f", colors)
        if normals is not None:
            self.vertex_layout.add_attribute("in_normal", "3f", normals)
        if texcoords is not None:
            self.vertex_layout.add_attribute("in_uv", "2f", texcoords)
