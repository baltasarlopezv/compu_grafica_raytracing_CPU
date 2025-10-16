from moderngl import Attribute, Uniform
import glm
import os


class ShaderProgram:
    def __init__(self, ctx, vertex_shader_path, fragment_shader_path):
        # Ruta absoluta al directorio actual (donde está shader_program.py)
        base_path = os.path.dirname(__file__)

        # Armar rutas completas a los shaders
        vertex_path = os.path.join(base_path, vertex_shader_path)
        fragment_path = os.path.join(base_path, fragment_shader_path)

        # Debug opcional (te muestra por consola dónde está buscando)
        print("Vertex shader:", os.path.abspath(vertex_path))
        print("Fragment shader:", os.path.abspath(fragment_path))

        # Leer los archivos shader
        with open(vertex_path, 'r') as file:
            vertex_shader = file.read()
        with open(fragment_path, 'r') as file:
            fragment_shader = file.read()

        # Crear el programa (lo que ya tenías después de esto)
        self.prog = ctx.program(vertex_shader=vertex_shader, fragment_shader=fragment_shader)






        #####
        attributes = []
        uniforms = []
        for name in self.prog:
            member = self.prog[name]
            if type(member) is Attribute:
                attributes.append(name)
            if type(member) is Uniform:
                uniforms.append(name)
        
        self.attributes = list(attributes)
        self.uniforms = uniforms
    
    def set_uniform(self, name, value):
        if name in self.uniforms:
            uniform = self.prog[name]
            if isinstance(value, glm.mat4):
                uniform.write(value.to_bytes())
            elif hasattr(uniform, "value"):
                uniform.value = value

class ComputeShaderProgram:
    def __init__(self, ctx, compute_shader_path):
        # Ruta absoluta al directorio actual (donde está shader_program.py)
        base_path = os.path.dirname(__file__)
        
        # Armar ruta completa al compute shader
        compute_path = os.path.join(base_path, compute_shader_path)
        
        print("Compute shader:", os.path.abspath(compute_path))
        
        with open(compute_path) as file:
            compute_source = file.read()
        
        try:
            self.prog = ctx.compute_shader(compute_source)
        except Exception as e:
            print(f"Error compiling compute shader: {e}")
            print(f"Shader source:\n{compute_source}")
            raise
        
        uniforms = []
        for name in self.prog:
            member = self.prog[name]
            if type(member) is Uniform:
                uniforms.append(name)
        
        self.uniforms = uniforms
    
    def set_uniform(self, name, value):
        if name in self.uniforms:
            uniform = self.prog[name]
            if isinstance(value, glm.mat4):
                uniform.write(value.to_bytes())
            elif hasattr(uniform, "value"):
                uniform.value = value
    
    def run(self, groups_x, groups_y, groups_z = 1):
        self.prog.run(group_x = groups_x, group_y = groups_y, group_z = groups_z)