import os
import sys
import keyboard
import curses
import math
import time

from Command_Line_Font import command_line_font


command_line_font(6)        # Console ASCII font size
nScreenWidth = 200          # Console Screen Size X (columns)
nScreenHeight = 100          # Console Screen Size Y (rows)

# Create Screen Buffer
screen = [[' ' for x in range(nScreenWidth)] for y in range(nScreenHeight)]
os.system(f"mode con: cols={nScreenWidth*2} lines={nScreenHeight}") # Font mechanic(y is always twice as big as x)
view = curses.initscr()

# Initiate time variables
tp1 = time.perf_counter()
tp2 = time.perf_counter()

theta = 0

def draw(x, y):
    # Check screen boundry
    if x < nScreenWidth and y < nScreenHeight:
        screen[y][x] = u'\u2588'



def draw_line(x1, y1, x2, y2):
    dx = x2 - x1
    dy = y2 - y1
    dx1 = abs(dx)
    dy1 = abs(dy)
    px = 2 * dy1 - dx1
    py = 2 * dx1 - dy1

    if dy1 <= dx1:
        if dx >= 0:
            x = x1
            y = y1
            xe = x2

        else:
            x = x2
            y = y2
            xe = x1
        draw(x, y)
        for i in range(x, xe):
            x += 1
            if px < 0:
                px = px + 2 * dy1
            
            else:
                if (dx < 0 and dy < 0) or (dx > 0 and dy > 0):
                    y = y + 1

                else:
                    y = y - 1
                px = px + 2 * (dy1 - dx1)
            draw(x, y)
    
    else:
        if dy >= 0:
            x = x1
            y = y1
            ye = y2
        
        else:
            x = x2
            y = y2
            ye = y1
        draw(x, y)
        for i in range(y, ye):
            y += 1
            if py <= 0:
                py = py + 2 * dx1
            
            else:
                if (dx < 0 and dy < 0) or (dx > 0 and dy > 0):
                    x = x + 1
                
                else:
                    x = x - 1
                py = py + 2 * (dx1 - dy1)
            draw(x, y)

def draw_triangle(x1, y1, x2, y2, x3, y3):
    draw_line(x1, y1, x2, y2)
    draw_line(x2, y2, x3, y3)
    draw_line(x3, y3, x1, y1)

class Vec_3D():
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

class Triangle():
    def __init__(self, vec_1, vec_2, vec_3):
        self.vec_1 = vec_1
        self.vec_2 = vec_2
        self.vec_3 = vec_3

# class Mesh():

#     tris = [Triangle()]

class Mat4x4():
    def __init__(self):
        self.matrix = [[0 for x in range(4)] for y in range(4)]

class Cube_Mesh():

    tris = [

        # South
        Triangle(Vec_3D(0, 0, 0), Vec_3D(0, 1, 0), Vec_3D(1, 1, 0)),
        Triangle(Vec_3D(0, 0, 0), Vec_3D(1, 1, 0), Vec_3D(1, 0, 0)),

        # East
        Triangle(Vec_3D(1, 0, 0), Vec_3D(1, 1, 0), Vec_3D(1, 1, 1)),
        Triangle(Vec_3D(1, 0, 0), Vec_3D(1, 1, 1), Vec_3D(1, 0, 1)),

        # North
        Triangle(Vec_3D(1, 0, 1), Vec_3D(1, 1, 1), Vec_3D(0, 1, 1)),
        Triangle(Vec_3D(1, 0, 1), Vec_3D(0, 1, 1), Vec_3D(0, 0, 1)),

        # West
        Triangle(Vec_3D(0, 0, 1), Vec_3D(0, 1, 1), Vec_3D(0, 1, 0)),
        Triangle(Vec_3D(0, 0, 1), Vec_3D(0, 1, 0), Vec_3D(0, 0, 0)),

        # Top
        Triangle(Vec_3D(0, 1, 0), Vec_3D(0, 1, 1), Vec_3D(1, 1, 1)),
        Triangle(Vec_3D(0, 1, 0), Vec_3D(1, 1, 1), Vec_3D(1, 1, 0)),

        # Bottom
        Triangle(Vec_3D(1, 0, 1), Vec_3D(0, 0, 1), Vec_3D(0, 0, 0)),
        Triangle(Vec_3D(1, 0, 1), Vec_3D(0, 0, 0), Vec_3D(1, 0, 0)),
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



def multiply_matrix_vector(vec_3d, triangle, point, mat4x4):
    if point == 1:
        triangle.vec_1.x = vec_3d.x * mat4x4.matrix[0][0] + vec_3d.y * mat4x4.matrix[1][0] + vec_3d.z * mat4x4.matrix[2][0] + mat4x4.matrix[3][0]
        triangle.vec_1.y = vec_3d.x * mat4x4.matrix[0][1] + vec_3d.y * mat4x4.matrix[1][1] + vec_3d.z * mat4x4.matrix[2][1] + mat4x4.matrix[3][1]
        triangle.vec_1.z = vec_3d.x * mat4x4.matrix[0][2] + vec_3d.y * mat4x4.matrix[1][2] + vec_3d.z * mat4x4.matrix[2][2] + mat4x4.matrix[3][2]
        w = vec_3d.x * mat4x4.matrix[0][3] + vec_3d.y * mat4x4.matrix[1][3] + vec_3d.z * mat4x4.matrix[2][3] + mat4x4.matrix[3][3]

        if w != 0:
            triangle.vec_1.x /= w
            triangle.vec_1.y /= w
            triangle.vec_1.z /= w

    elif point == 2:
        triangle.vec_2.x = vec_3d.x * mat4x4.matrix[0][0] + vec_3d.y * mat4x4.matrix[1][0] + vec_3d.z * mat4x4.matrix[2][0] + mat4x4.matrix[3][0]
        triangle.vec_2.y = vec_3d.x * mat4x4.matrix[0][1] + vec_3d.y * mat4x4.matrix[1][1] + vec_3d.z * mat4x4.matrix[2][1] + mat4x4.matrix[3][1]
        triangle.vec_2.z = vec_3d.x * mat4x4.matrix[0][2] + vec_3d.y * mat4x4.matrix[1][2] + vec_3d.z * mat4x4.matrix[2][2] + mat4x4.matrix[3][2]
        w = vec_3d.x * mat4x4.matrix[0][3] + vec_3d.y * mat4x4.matrix[1][3] + vec_3d.z * mat4x4.matrix[2][3] + mat4x4.matrix[3][3]

        if w != 0:
            triangle.vec_2.x /= w
            triangle.vec_2.y /= w
            triangle.vec_2.z /= w
    
    else:
        triangle.vec_3.x = vec_3d.x * mat4x4.matrix[0][0] + vec_3d.y * mat4x4.matrix[1][0] + vec_3d.z * mat4x4.matrix[2][0] + mat4x4.matrix[3][0]
        triangle.vec_3.y = vec_3d.x * mat4x4.matrix[0][1] + vec_3d.y * mat4x4.matrix[1][1] + vec_3d.z * mat4x4.matrix[2][1] + mat4x4.matrix[3][1]
        triangle.vec_3.z = vec_3d.x * mat4x4.matrix[0][2] + vec_3d.y * mat4x4.matrix[1][2] + vec_3d.z * mat4x4.matrix[2][2] + mat4x4.matrix[3][2]
        w = vec_3d.x * mat4x4.matrix[0][3] + vec_3d.y * mat4x4.matrix[1][3] + vec_3d.z * mat4x4.matrix[2][3] + mat4x4.matrix[3][3]

        if w != 0:
            triangle.vec_3.x /= w
            triangle.vec_3.y /= w
            triangle.vec_3.z /= w



while 1:

    # Reset screen
    screen = [[' ' for x in range(nScreenWidth)] for y in range(nScreenHeight)]     

    # Quit simulation
    if keyboard.is_pressed('Q'):
        curses.endwin()                                 # End curses instance
        os.system(f"mode con: cols={120} lines={40}")   # Reset screen buffer
        command_line_font(16)                           # Reset default font size
        sys.exit()                                      # Exit Program

    # Rotation Simulation
    mat_rot_z = Mat4x4()
    mat_rot_x = Mat4x4()

    # Calculate time differential per frame
    tp2 = time.perf_counter()
    elapsed_time = tp2 - tp1
    tp1 = tp2
    elapsed_time = elapsed_time

    theta += 1 * elapsed_time

    # Rotation Z matrix
    mat_rot_z.matrix[0][0] = math.cos(theta)
    mat_rot_z.matrix[0][1] = math.sin(theta)
    mat_rot_z.matrix[1][0] = -math.sin(theta)
    mat_rot_z.matrix[1][1] = math.cos(theta)
    mat_rot_z.matrix[2][2] = 1
    mat_rot_z.matrix[3][3] = 1

    # Rotation X matrix
    mat_rot_x.matrix[0][0] = 1
    mat_rot_x.matrix[1][1] = math.cos(theta * 0.5)
    mat_rot_x.matrix[1][2] = math.sin(theta * 0.5)
    mat_rot_x.matrix[2][1] = -math.sin(theta * 0.5)
    mat_rot_x.matrix[2][2] = math.cos(theta * 0.5)
    mat_rot_x.matrix[3][3] = 1


    # Iterate through predefined triangles
    for tri in Cube_Mesh.tris:
        # Initiate output projected triangle
        tri_projected = Triangle(Vec_3D(), Vec_3D(), Vec_3D())
        tri_rotated_z = Triangle(Vec_3D(), Vec_3D(), Vec_3D())
        tri_rotated_zx = Triangle(Vec_3D(), Vec_3D(), Vec_3D())
        
        # Rotate Z
        multiply_matrix_vector(tri.vec_1, tri_rotated_z, 1, mat_rot_z)
        multiply_matrix_vector(tri.vec_2, tri_rotated_z, 2, mat_rot_z)
        multiply_matrix_vector(tri.vec_3, tri_rotated_z, 3, mat_rot_z)

        # Rotate X
        multiply_matrix_vector(tri_rotated_z.vec_1, tri_rotated_zx, 1, mat_rot_x)
        multiply_matrix_vector(tri_rotated_z.vec_2, tri_rotated_zx, 2, mat_rot_x)
        multiply_matrix_vector(tri_rotated_z.vec_3, tri_rotated_zx, 3, mat_rot_x)

        # Offset triangle into the screen
        tri_translated = Triangle(Vec_3D(tri_rotated_zx.vec_1.x, tri_rotated_zx.vec_1.y, tri_rotated_zx.vec_1.z), Vec_3D(tri_rotated_zx.vec_2.x, tri_rotated_zx.vec_2.y, tri_rotated_zx.vec_2.z), Vec_3D(tri_rotated_zx.vec_3.x, tri_rotated_zx.vec_3.y, tri_rotated_zx.vec_3.z))

        tri_translated.vec_1.z = tri_rotated_zx.vec_1.z + 3
        tri_translated.vec_2.z = tri_rotated_zx.vec_2.z + 3
        tri_translated.vec_3.z = tri_rotated_zx.vec_3.z + 3

        # Calculate projected triangle vlaues
        multiply_matrix_vector(tri_translated.vec_1, tri_projected, 1, Cube_Mesh.matrix_prog)
        multiply_matrix_vector(tri_translated.vec_2, tri_projected, 2, Cube_Mesh.matrix_prog)
        multiply_matrix_vector(tri_translated.vec_3, tri_projected, 3, Cube_Mesh.matrix_prog)

        # Scale into view
        tri_projected.vec_1.x += 1
        tri_projected.vec_1.y += 1
        tri_projected.vec_2.x += 1
        tri_projected.vec_2.y += 1
        tri_projected.vec_3.x += 1
        tri_projected.vec_3.y += 1
        tri_projected.vec_1.x *= 0.5 * nScreenWidth
        tri_projected.vec_1.y *= 0.5 * nScreenHeight
        tri_projected.vec_2.x *= 0.5 * nScreenWidth
        tri_projected.vec_2.y *= 0.5 * nScreenHeight
        tri_projected.vec_3.x *= 0.5 * nScreenWidth
        tri_projected.vec_3.y *= 0.5 * nScreenHeight

        # Draw and Contribute traingle lines to screen
        draw_triangle(int(tri_projected.vec_1.x), int(tri_projected.vec_1.y), int(tri_projected.vec_2.x), int(tri_projected.vec_2.y), int(tri_projected.vec_3.x), int(tri_projected.vec_3.y))



    # Display Frame (problem with the \0 in python 3.9. empty string also works. null termination only needed for c++ version)
    screen[nScreenHeight - 1][nScreenWidth - 1] = ''
    view.addstr(0, 0, ''.join(ele + ele for sub in screen for ele in sub))
    view.refresh()
