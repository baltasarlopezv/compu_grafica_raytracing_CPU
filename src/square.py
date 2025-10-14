from model import Model
import numpy as np
import glm

class Square(Model):
    def __init__(self, position=(0,0,0), rotation=(0,0,0), scale=(1,1,1), name="square", hittable=True):
        self.name = name
        self.position = glm.vec3(*position)
        self.rotation = glm.vec3(*rotation)
        self.scale = glm.vec3(*scale)
        
        # Separar posiciones y colores
        vertices = np.array([
            -1.0, -1.0, 0.0,  # bottom left
             1.0, -1.0, 0.0,  # bottom right
             1.0,  1.0, 0.0,  # top right
            -1.0,  1.0, 0.0,  # top left
        ], dtype='f4')
        
        colors = np.array([
            1.0, 0.0, 0.0,  # red
            0.0, 1.0, 0.0,  # green
            0.0, 0.0, 1.0,  # blue
            1.0, 1.0, 0.0,  # yellow
        ], dtype='f4')
        
        # Indices for two triangles that make a square
        indices = np.array([
            0, 1, 2,  # first triangle
            0, 2, 3   # second triangle
        ], dtype='i4')
        
        # Llamar al constructor de Model
        super().__init__(vertices=vertices, indices=indices, colors=colors)
    
    def get_model_matrix(self):
        model = glm.mat4(1)
        model = glm.translate(model, self.position)
        model = glm.rotate(model, glm.radians(self.rotation.x), glm.vec3(1, 0, 0))
        model = glm.rotate(model, glm.radians(self.rotation.y), glm.vec3(0, 1, 0))
        model = glm.rotate(model, glm.radians(self.rotation.z), glm.vec3(0, 0, 1))
        model = glm.scale(model, self.scale)
        return model
