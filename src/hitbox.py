import glm

class Hitbox:
    def __init__(self, center=(0,0,0), size=(1,1,1)):
        self.center = glm.vec3(*center)
        self.size = glm.vec3(*size)
    
    def intersect(self, ray):
        # Intersección rayo-caja alineada a ejes (AABB)
        # Calcular los límites de la caja
        min_bounds = self.center - self.size * 0.5
        max_bounds = self.center + self.size * 0.5
        
        # Calcular las distancias de intersección para cada eje
        t_min = (min_bounds - ray.origin) / ray.direction
        t_max = (max_bounds - ray.origin) / ray.direction
        
        # Asegurar que t_min <= t_max para cada eje
        for i in range(3):
            if t_min[i] > t_max[i]:
                t_min[i], t_max[i] = t_max[i], t_min[i]
        
        # Encontrar la intersección más cercana y lejana
        t_near = max(t_min.x, t_min.y, t_min.z)
        t_far = min(t_max.x, t_max.y, t_max.z)
        
        # Verificar si hay intersección
        if t_near > t_far or t_far < 0:
            return None
        
        # Retornar la distancia de intersección
        t = t_near if t_near >= 0 else t_far
        return t if t >= 0 else None