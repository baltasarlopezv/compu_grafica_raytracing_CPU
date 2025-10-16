from graphics import Graphics
from raytracer import RayTracer
import glm
import math
import numpy as np
from raytracer import RayTracerGPU
from graphics import ComputeGraphics

class Scene:
    """
    Escena básica con renderizado tradicional (raycasting).
    """
    def __init__(self, ctx, camera):
        self.ctx = ctx
        self.objects = []
        self.graphics = {}
        self.camera = camera
        self.time = 0.0
        self.view = self.camera.get_view_matrix()
        self.projection = self.camera.get_perspective_matrix()
    
    def add_object(self, model, material):
        """Agrega un objeto a la escena."""
        self.objects.append(model)
        self.graphics[model.name] = Graphics(self.ctx, model, material)
    
    def start(self):
        print("Start!")
    
    def on_mouse_click(self, u, v):
        ray = self.camera.raycast(u, v)
        for obj in self.objects:
            if obj.check_hit(ray.origin, ray.direction):
                print(f"¡Golpeaste al objeto {obj.name}!")
    
    def render(self):
        # Limpiar la pantalla
        self.ctx.clear(0.1, 0.1, 0.1, 1.0)
        self.ctx.enable(self.ctx.DEPTH_TEST)
        
        # Delta time fijo para animaciones suaves
        delta_time = 0.016  # ~60 FPS
        
        for obj in self.objects:
            # Actualizar animación del objeto
            if hasattr(obj, 'update'):
                obj.update(delta_time)
            
            # Renderizar objeto
            model = obj.get_model_matrix()
            mvp = self.projection * self.view * model
            self.graphics[obj.name].render({'Mvp': mvp})
    
    def on_resize(self, width, height):
        self.ctx.viewport = (0, 0, width, height)
        self.camera.aspect = width / height if height != 0 else 1.0


class RayScene(Scene):
    def __init__(self, ctx, camera, width, height):
        super().__init__(ctx, camera)
        self.raytracer = RayTracer(camera, width, height)
    
    def start(self):
        self.raytracer.render_frame(self.objects)
        if "Sprite" in self.graphics:
            self.graphics["Sprite"].update_texture("u_texture", self.raytracer.get_texture())
    
    def render(self):
        super().render()
    
    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.raytracer = RayTracer(self.camera, width, height)
        self.start()

class RaySceneGPU(Scene):
    def __init__(self, ctx, camera, width, height, output_model, output_material):
        self.ctx = ctx
        self.camera = camera
        self.width = width
        self.height = height
        self.raytracer = None

        self.output_graphics = Graphics(ctx, output_model, output_material)
        self.raytracer = RayTracerGPU(self.ctx, self.camera, self.width, self.height, self.output_graphics)
        super().__init__(self.ctx, self.camera)
    
    def add_object(self, model, material):
        self.objects.append(model)
        self.graphics[model.name] = ComputeGraphics(self.ctx, model, material)

    def start(self):
        print("Start!")
        self.primitives = []
        n = len(self.objects)
        self.models_f = np.zeros((n, 16), dtype='f4')
        self.inv_f = np.zeros((n, 16), dtype='f4')
        self.mats_f = np.zeros((n, 4), dtype='f4')  # reflectividad + colorRGB

        self._update_matrix()
        self._matrix_to_ssbo()

    def render(self):
        # Delta time fijo para animaciones suaves
        delta_time = 0.016  # ~60 FPS
        
        for obj in self.objects:
            # Actualizar animación del objeto
            if hasattr(obj, 'update'):
                obj.update(delta_time)
        
        if(self.raytracer is not None):
            self._update_matrix()
            self._matrix_to_ssbo()
            self.raytracer.run()

    def on_resize(self, width, height):
        super().on_resize(width, height)
        self.width, self.height = width, height
        self.camera.aspect = width / height if height != 0 else 1.0

    def _update_matrix(self):
        self.primitives = []

        for i, (name, graphics) in enumerate(self.graphics.items()):
            graphics.create_primitive(self.primitives)
            graphics.create_transformation_matrix(self.models_f, i)
            graphics.create_inverse_transformation_matrix(self.inv_f, i)
            graphics.create_material_matrix(self.mats_f, i)

    def _matrix_to_ssbo(self):
        self.raytracer.matrix_to_ssbo(self.models_f, 0)
        self.raytracer.matrix_to_ssbo(self.inv_f, 1)
        self.raytracer.matrix_to_ssbo(self.mats_f, 2)
        self.raytracer.primitives_to_ssbo(self.primitives, 3)