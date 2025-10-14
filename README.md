# Proyecto de Raytracing en CPU

Este proyecto implementa un motor de raytracing básico en CPU utilizando Python, OpenGL y ModernGL.

## Requisitos

- Python 3.13 o superior
- Entorno virtual de Python (incluido)

## Dependencias

- `moderngl` (5.12.0) - Biblioteca de OpenGL moderna para Python
- `PyGLM` (2.8.2) - Biblioteca de matemáticas para gráficos 3D
- `numpy` (2.3.3) - Cálculos numéricos y manejo de arrays
- `pyglet` (2.1.9) - Creación de ventanas y manejo de eventos

## Instalación

Las dependencias ya están instaladas en el entorno virtual `.venv`. Si necesitas reinstalarlas:

```bash
# Activar el entorno virtual
source .venv/bin/activate  # En macOS/Linux
# o
.venv\Scripts\activate  # En Windows

# Instalar dependencias
pip install moderngl PyGLM numpy pyglet
```

## Ejecución

Para ejecutar el proyecto:

```bash
# Desde la raíz del proyecto
.venv/bin/python src/main.py
```

O si tienes el entorno virtual activado:

```bash
python src/main.py
```

## Estructura del Proyecto

```
├── src/
│   ├── main.py           # Punto de entrada del programa
│   ├── window.py         # Manejo de la ventana con Pyglet
│   ├── scene.py          # Gestión de la escena y RayScene
│   ├── camera.py         # Cámara con raycast y gradientes de cielo
│   ├── raytracer.py      # Motor de raytracing en CPU
│   ├── model.py          # Clases base para modelos 3D
│   ├── cube.py           # Modelo de cubo
│   ├── quad.py           # Modelo de plano (para mostrar textura)
│   ├── sphere.py         # Modelo de esfera
│   ├── square.py         # Modelo de cuadrado
│   ├── graphics.py       # Gestión de buffers y renderizado OpenGL
│   ├── material.py       # Material (shader + texturas)
│   ├── texture.py        # Manejo de texturas y ImageData
│   ├── shader_program.py # Compilación y gestión de shaders
│   ├── hit.py            # Sistema de detección de colisiones
│   └── ray.py            # Clase Ray para raytracing
├── shaders/
│   ├── basic.vert        # Vertex shader básico
│   ├── basic.frag        # Fragment shader básico
│   ├── sprite.vert       # Vertex shader para sprites/texturas
│   └── sprite.frag       # Fragment shader para sprites/texturas
└── .venv/                # Entorno virtual de Python
```

## Características

- **Raytracing en CPU**: Implementación básica de raytracing que genera una textura
- **Gradiente de cielo**: Fondo con degradado que simula el cielo
- **Detección de colisiones**: Sistema de hitboxes para rayos
- **Renderizado híbrido**: Raytracing en CPU + renderizado OpenGL en GPU
- **Sistema modular**: Arquitectura orientada a objetos con separación de responsabilidades

## Notas

- El raytracing se ejecuta en CPU, por lo que puede tardar unos segundos en generar la primera imagen (especialmente en resoluciones altas)
- Una vez generada la textura, el renderizado en GPU es fluido
- Los objetos aparecen en rojo cuando son impactados por un rayo
- El fondo muestra un gradiente de cielo azul

## Créditos

Proyecto desarrollado para el curso de Computación Gráfica, basado en las técnicas de "Raytracing in One Weekend".
