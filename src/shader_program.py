import moderngl

class ShaderProgram:
    def __init__(self, ctx, vertex_path, fragment_path):
        """
        Inicializa el programa de shaders cargando los archivos vertex y fragment.
        
        Args:
            ctx: Contexto de ModernGL
            vertex_path: Ruta al archivo del vertex shader
            fragment_path: Ruta al archivo del fragment shader
        """
        self.ctx = ctx
        
        # Cargar el código de los shaders desde archivos
        with open(vertex_path, 'r') as f:
            vertex_source = f.read()
        
        with open(fragment_path, 'r') as f:
            fragment_source = f.read()
        
        # Crear el programa de shaders
        self.program = self.ctx.program(
            vertex_shader=vertex_source,
            fragment_shader=fragment_source
        )
    
    def use(self):
        """Activa este programa de shaders para su uso."""
        pass  # En ModernGL no es necesario hacer bind explícito
    
    def set_uniform(self, name, value):
        """
        Establece el valor de un uniform del shader.
        
        Args:
            name: Nombre del uniform
            value: Valor a asignar
        """
        if name in self.program:
            self.program[name].write(value.tobytes())
    
    def get_program(self):
        """Retorna el objeto program de ModernGL."""
        return self.program