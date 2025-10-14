from graphics import Graphics
from raytracer import RayTracer
import glm
import math

class Scene:
    def __init__(self, ctx, camera):
        self.ctx = ctx
        self.objects = []
        self.graphics = {}
        self.camera = camera
        self.time = 0.0
        self.view = self.camera.get_view_matrix()
        self.projection = self.camera.get_perspective_matrix()
    
    def add_object(self, model, material):
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
        self.time += 0.01
        for obj in self.objects:
            if(obj.name != "Sprite"):
                obj.rotation += glm.vec3(0.8, 0.6, 0.4)
                obj.position.x += math.sin(self.time) * 0.01
            
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