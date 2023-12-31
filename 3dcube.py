import pygame
from pygame.locals import *
from OpenGL.GL import *
import pyrr

# Initialize Pygame
pygame.init()

# Set up display
display = (800, 600)
pygame.display.set_mode(display, DOUBLEBUF | OPENGL)

# Vertex shader source code
vertex_shader_source = """
#version 330 core
layout (location = 0) in vec3 aPos;

uniform mat4 model;
uniform mat4 view;
uniform mat4 projection;

void main()
{
    gl_Position = projection * view * model * vec4(aPos, 1.0);
}
"""

# Fragment shader source code
fragment_shader_source = """
#version 330 core
out vec4 FragColor;

void main()
{
    FragColor = vec4(1.0, 0.5, 0.2, 1.0);  // Orange color for simplicity
}
"""

# Compile shaders
vertex_shader = glCreateShader(GL_VERTEX_SHADER)
glShaderSource(vertex_shader, vertex_shader_source)
glCompileShader(vertex_shader)

fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
glShaderSource(fragment_shader, fragment_shader_source)
glCompileShader(fragment_shader)

# Create shader program
shader_program = glCreateProgram()
glAttachShader(shader_program, vertex_shader)
glAttachShader(shader_program, fragment_shader)
glLinkProgram(shader_program)
glUseProgram(shader_program)

# Set initial camera position
view = pyrr.matrix44.create_look_at(pyrr.Vector3([0, 0, 5]), pyrr.Vector3([0, 0, 0]), pyrr.Vector3([0, 1, 0]))
projection = pyrr.matrix44.create_perspective_projection(45.0, display[0] / display[1], 0.1, 50.0)
model = pyrr.matrix44.create_identity()

# Get uniform locations
view_loc = glGetUniformLocation(shader_program, "view")
projection_loc = glGetUniformLocation(shader_program, "projection")
model_loc = glGetUniformLocation(shader_program, "model")

# Cube vertices
vertices = [
    -0.5, -0.5, -0.5,
    0.5, -0.5, -0.5,
    0.5, 0.5, -0.5,
    -0.5, 0.5, -0.5,
    -0.5, -0.5, 0.5,
    0.5, -0.5, 0.5,
    0.5, 0.5, 0.5,
    -0.5, 0.5, 0.5
]

# Cube indices
indices = [
    0, 1, 2, 2, 3, 0,
    4, 5, 6, 6, 7, 4,
    0, 3, 7, 7, 4, 0,
    1, 2, 6, 6, 5, 1,
    0, 1, 5, 5, 4, 0,
    2, 3, 7, 7, 6, 2
]

# Create VAO, VBO, and EBO
vao = glGenVertexArrays(1)
vbo = glGenBuffers(1)
ebo = glGenBuffers(1)

glBindVertexArray(vao)

# Upload vertices
glBindBuffer(GL_ARRAY_BUFFER, vbo)
glBufferData(GL_ARRAY_BUFFER, 4 * len(vertices), (GLfloat * len(vertices))(*vertices), GL_STATIC_DRAW)

# Upload indices
glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
glBufferData(GL_ELEMENT_ARRAY_BUFFER, 4 * len(indices), (GLuint * len(indices))(*indices), GL_STATIC_DRAW)

# Specify vertex attributes
glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 3 * 4, ctypes.c_void_p(0))
glEnableVertexAttribArray(0)

# Unbind VAO, VBO, and EBO
glBindBuffer(GL_ARRAY_BUFFER, 0)
glBindVertexArray(0)

# Main game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    # Clear the screen
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Get mouse movement
    x, y = pygame.mouse.get_pos()
    dx, dy = x - display[0] // 2, y - display[1] // 2

    # Invert left and right controls
    dx = -dx

    # Update view matrix based on mouse movement
    view = pyrr.matrix44.create_look_at(pyrr.Vector3([dx * 0.005, dy * 0.005, 5]),
                                         pyrr.Vector3([0, 0, 0]),
                                         pyrr.Vector3([0, 1, 0]))

    # Set uniforms
    glUniformMatrix4fv(view_loc, 1, GL_FALSE, view)
    glUniformMatrix4fv(projection_loc, 1, GL_FALSE, projection)
    glUniformMatrix4fv(model_loc, 1, GL_FALSE, model)

    # Draw cube
    glBindVertexArray(vao)
    glDrawElements(GL_TRIANGLES, len(indices), GL_UNSIGNED_INT, None)
    glBindVertexArray(0)

    # Update the display
    pygame.display.flip()

    # Manage frame rate
    pygame.time.Clock().tick(30)
