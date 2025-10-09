import numpy as np
import glm

class Square:
    def __init__(self, position=(0,0,0), rotation=(0,0,0), scale=(1,1,1), name="square"):
        self.name = name
        self.position = glm.vec3(*position)
        self.rotation = glm.vec3(*rotation)
        self.scale = glm.vec3(*scale)
        
        # Simple square vertices: position (3f) + color (3f)
        # A square in the XY plane from -1 to 1
        self.vertices = np.array([
            # positions     # colors
            -1.0, -1.0, 0.0,  1.0, 0.0, 0.0,  # bottom left - red
             1.0, -1.0, 0.0,  0.0, 1.0, 0.0,  # bottom right - green
             1.0,  1.0, 0.0,  0.0, 0.0, 1.0,  # top right - blue
            -1.0,  1.0, 0.0,  1.0, 1.0, 0.0,  # top left - yellow
        ], dtype='f4')
        
        # Indices for two triangles that make a square
        self.indices = np.array([
            0, 1, 2,  # first triangle
            0, 2, 3   # second triangle
        ], dtype='i4')
    
    def get_model_matrix(self):
        model = glm.mat4(1)
        model = glm.translate(model, self.position)
        model = glm.rotate(model, glm.radians(self.rotation.x), glm.vec3(1, 0, 0))
        model = glm.rotate(model, glm.radians(self.rotation.y), glm.vec3(0, 1, 0))
        model = glm.rotate(model, glm.radians(self.rotation.z), glm.vec3(0, 0, 1))
        model = glm.scale(model, self.scale)
        return model
