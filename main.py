import os
import sys
import keyboard
import curses
import math

from Command_Line_Font import command_line_font


command_line_font(16)        # Console ASCII font size
nScreenWidth = 100          # Console Screen Size X (columns)
nScreenHeight = 40          # Console Screen Size Y (rows)

# Create Screen Buffer
screen = [[' ' for x in range(nScreenWidth)] for y in range(nScreenHeight)]
os.system(f"mode con: cols={nScreenWidth*2} lines={nScreenHeight}") # Font mechanic(y is always twice as big as x)
view = curses.initscr()

class Vec_3D():

    x = 0
    y = 0
    z = 0

class Triangle():

    points = [Vec_3D(), Vec_3D(), Vec_3D()]

class Mesh():

    tris = [Triangle()]

class Mat4x4():

    matrix = [[0 for x in range(4)] for y in range(4)]

class Cube_Mesh():

    tris = [

        # South
        [0, 0, 0,       0, 1, 0,        1, 1, 0],
        [0, 0, 0,       1, 1, 0,        1, 0, 0],

        # East
        [1, 0, 0,       1, 1, 0,        1, 1, 1],
        [1, 0, 0,       1, 1, 1,        1, 0, 1],

        # North
        [1, 0, 1,       1, 1, 1,        0, 1, 1],
        [1, 0, 1,       0, 1, 1,        0, 0, 1],

        # West
        [0, 0, 1,       0, 1, 1,        0, 1, 0],
        [0, 0, 1,       0, 1, 0,        0, 0, 0],

        # Top
        [0, 1, 0,       0, 1, 1,        1, 1, 1],
        [0, 1, 0,       1, 1, 1,        1, 1, 0],

        # Bottom
        [1, 0, 1,       0, 0, 1,        0, 0, 0],
        [1, 0, 1,       0, 0, 0,        1, 0, 0]
    ]

    # Projection Matrix
    near = 0.1
    far = 1000
    fov = 90
    aspect_ratio = nScreenHeight / nScreenWidth
    fov_rad = 1 / math.atan(fov * 0.5 / 180 * 3.14159)

    matrix_prog = Mat4x4()
    matrix_prog.matrix[0][0] = aspect_ratio * fov_rad
    matrix_prog.matrix[1][1] = fov_rad
    matrix_prog.matrix[2][2] = far / (far - near)
    matrix_prog.matrix[3][2] = (-far * near) / (far - near)
    matrix_prog.matrix[2][3] = 1
    matrix_prog.matrix[3][3] = 0



def multiply_matrix_vector(vec_3d, triangle, mat4x4):
    triangle.points[0].x = vec_3d.x * mat4x4.matrix[0][0] + vec_3d.y * mat4x4.matrix[1][0] + vec_3d.z * mat4x4.matrix[2][0] + mat4x4.matrix[3][0]
    triangle.points[1].y = vec_3d.x * mat4x4.matrix[0][1] + vec_3d.y * mat4x4.matrix[1][1] + vec_3d.z * mat4x4.matrix[2][1] + mat4x4.matrix[3][1]
    triangle.points[2].z = vec_3d.x * mat4x4.matrix[0][2] + vec_3d.y * mat4x4.matrix[1][2] + vec_3d.z * mat4x4.matrix[2][2] + mat4x4.matrix[3][2]
    w = vec_3d.x * mat4x4.matrix[0][3] + vec_3d.y * mat4x4.matrix[1][3] + vec_3d.z * mat4x4.matrix[2][3] + mat4x4.matrix[3][3]

    if w != 0:
        triangle.points[0].x /= w
        triangle.points[1].y /= w
        triangle.points[2].z /= w

while 1:

    # Quit simulation
    if keyboard.is_pressed('Q'):
        curses.endwin()                                 # End curses instance
        os.system(f"mode con: cols={120} lines={40}")   # Reset screen buffer
        command_line_font(16)                           # Reset default font size
        sys.exit()                                      # Exit Program

    # Draw Triangles
    for tri in Cube_Mesh.tris:
        tri_projected = Triangle()

        multiply_matrix_vector(tri.)

    # Testing
    screen[20][40] = 'T'

    # Display Frame (problem with the \0 in python 3.9. empty string also works. null termination only needed for c++ version)
    screen[nScreenHeight - 1][nScreenWidth - 1] = ''
    view.addstr(0, 0, ''.join(ele + ele for sub in screen for ele in sub))
    view.refresh()
