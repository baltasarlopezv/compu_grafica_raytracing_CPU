import numpy as np
import glm

class Sphere:
    def __init__(self, position=(0,0,0), rotation=(0,0,0), scale=(1,1,1), name="sphere", sectors=24, stacks=16):
        self.name = name
        self.position = glm.vec3(*position)
        self.rotation = glm.vec3(*rotation)
        self.scale = glm.vec3(*scale)

        vertices = []
        indices = []
        pi = np.pi
        for i in range(stacks + 1):
            stack_angle = pi / 2 - i * pi / stacks  # from pi/2 to -pi/2
            xy = np.cos(stack_angle)
            z = np.sin(stack_angle)
            for j in range(sectors + 1):
                sector_angle = j * 2 * pi / sectors  # from 0 to 2pi
                x = xy * np.cos(sector_angle)
                y = xy * np.sin(sector_angle)
                # Interleave position and color for each vertex
                r = (x + 1) / 2
                g = (y + 1) / 2
                b = (z + 1) / 2
                vertices.extend([x, y, z, r, g, b])
        # Indices
        for i in range(stacks):
            for j in range(sectors):
                first = i * (sectors + 1) + j
                second = first + sectors + 1
                indices.extend([first, second, first + 1])
                indices.extend([second, second + 1, first + 1])
        self.vertices = np.array(vertices, dtype='f4')
        self.indices = np.array(indices, dtype='i4')

    def get_model_matrix(self):
        model = glm.mat4(1)
        model = glm.translate(model, self.position)
        model = glm.rotate(model, glm.radians(self.rotation.x), glm.vec3(1, 0, 0))
        model = glm.rotate(model, glm.radians(self.rotation.y), glm.vec3(0, 1, 0))
        model = glm.rotate(model, glm.radians(self.rotation.z), glm.vec3(0, 0, 1))
        model = glm.scale(model, self.scale)
        return model

    def update(self, delta_time):
        pass
