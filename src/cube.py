from model import Model
from hit import HitBoxOBB
import numpy as np
import glm


class Cube(Model):
    """
    Representa un cubo 3D en la escena.
    Hereda de Model para manejar vértices, índices y texturas.
    """
    def __init__(self, position=(0,0,0), rotation=(0,0,0), scale=(1,1,1), name="cube", animated=True, hittable=True):
        self.name = name
        self.animated = animated
        self.position = glm.vec3(*position)
        self.rotation = glm.vec3(*rotation)
        self.scale = glm.vec3(*scale)
        self.__colision = HitBoxOBB(get_model_matrix=lambda: self.get_model_matrix(), hittable=hittable)

        # Array para crear el VBO: Vertex Buffer Object: almacena los vértices del cubo
        vertices = np.array([
            -1,-1,-1,  1,-1,-1,  1,1,-1, -1,1,-1,
            -1,-1,1,   1,-1,1,   1,1,1,  -1,1,1
        ], dtype='f4')

        # Colores para cada vértice del cubo
        colors = np.array([
            1,0,0, 0,1,0, 0,0,1, 1,1,0,
            1,0,1, 0,1,1, 1,1,1, 0,0,0
        ], dtype='f4')


        # Normales para iluminación
        normals = np.array([
            -1,-1,-1,  1,-1,-1,  1,1,-1, -1,1,-1,
            -1,-1,1,   1,-1,1,   1,1,1,  -1,1,1
        ], dtype='f4')


        # Coordenadas de textura (UV)
        texcoords = np.array([
            0,0, 1,0, 1,1, 0,1,
            0,0, 1,0, 1,1, 0,1
        ], dtype='f4')


        # Array para crear el IBO: Index Buffer Object: define las caras del cubo
        indices = np.array([
            0,1,2, 2,3,0, 4,5,6, 6,7,4,
            0,4,7, 7,3,0, 1,5,6, 6,2,1,
            3,2,6, 6,7,3, 0,1,5, 5,4,0
        ], dtype='i4')

        self.__vertices = vertices
        super().__init__(vertices, indices, colors, normals, texcoords)

    @property
    def aabb(self):
        verts3 = self.__vertices.reshape(-1, 3)

        pts = [self.get_model_matrix() * glm.vec4(v[0], v[1], v[2], 1.0) for v in verts3]
        xs = [p.x for p in pts]
        ys = [p.y for p in pts]
        zs = [p.z for p in pts]
        return (glm.vec3(min(xs), min(ys), min(zs)),
                glm.vec3(max(xs), max(ys), max(zs)))

    def check_hit(self, origin, direction):
        return self.__colision.check_hit(origin, direction)
   
    def update(self, delta_time):
        """
        Actualiza la rotación del cubo para crear una animación.
        """
        if self.animated:
            self.rotation.x += 30 * delta_time  # 30 grados por segundo en X
            self.rotation.y += 45 * delta_time  # 45 grados por segundo en Y
            self.rotation.z += 20 * delta_time  # 20 grados por segundo en Z
   
    def get_model_matrix(self):
        model = glm.mat4(1)
        model = glm.translate(model, self.position)
        model = glm.rotate(model, glm.radians(self.rotation.x % 360), glm.vec3(1, 0, 0))
        model = glm.rotate(model, glm.radians(self.rotation.y % 360), glm.vec3(0, 1, 0))
        model = glm.rotate(model, glm.radians(self.rotation.z % 360), glm.vec3(0, 0, 1))
        model = glm.scale(model, self.scale)
        return model