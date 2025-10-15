#version 330 core

// Atributos de entrada
layout (location = 0) in vec3 in_pos;
layout (location = 1) in vec3 in_color;

// Uniform para la matriz MVP
uniform mat4 Mvp;

// Variable de salida al fragment shader
out vec3 v_color;

void main() {
    // Transformar la posición del vértice usando la matriz MVP
    gl_Position = Mvp * vec4(in_pos, 1.0);
    
    // Pasar el color al fragment shader
    v_color = in_color;
}