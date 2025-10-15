#version 330 core

// Variable de entrada desde el vertex shader
in vec3 v_color;

// Color de salida del fragmento
out vec4 out_color;

void main() {
    // Asignar el color interpolado al fragmento con alpha 1.0 (opaco)
    out_color = vec4(v_color, 1.0);
}