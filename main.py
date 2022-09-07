'''Graphical Rendering in The Command Line'''

import sys
import math
import time

import keyboard

from console_render_engine import ConsoleRenderEngine
from mesh_classes import Vector, Triangle, ProjectionMatrix, CubeMesh, Mesh


def multiply_matrix_vector(vector, triangle, point, projection_matrix):
    '''Matrix multiplication for projecting 3D data on to 2D matrix'''
    if point == 1:
        triangle.vec_1.x = vector.x * projection_matrix.matrix[0][0] + vector.y * projection_matrix.matrix[1][0] + vector.z * projection_matrix.matrix[2][0] + projection_matrix.matrix[3][0]
        triangle.vec_1.y = vector.x * projection_matrix.matrix[0][1] + vector.y * projection_matrix.matrix[1][1] + vector.z * projection_matrix.matrix[2][1] + projection_matrix.matrix[3][1]
        triangle.vec_1.z = vector.x * projection_matrix.matrix[0][2] + vector.y * projection_matrix.matrix[1][2] + vector.z * projection_matrix.matrix[2][2] + projection_matrix.matrix[3][2]
        w = vector.x * projection_matrix.matrix[0][3] + vector.y * projection_matrix.matrix[1][3] + vector.z * projection_matrix.matrix[2][3] + projection_matrix.matrix[3][3]

        if w != 0:
            triangle.vec_1.x /= w
            triangle.vec_1.y /= w
            triangle.vec_1.z /= w

    elif point == 2:
        triangle.vec_2.x = vector.x * projection_matrix.matrix[0][0] + vector.y * projection_matrix.matrix[1][0] + vector.z * projection_matrix.matrix[2][0] + projection_matrix.matrix[3][0]
        triangle.vec_2.y = vector.x * projection_matrix.matrix[0][1] + vector.y * projection_matrix.matrix[1][1] + vector.z * projection_matrix.matrix[2][1] + projection_matrix.matrix[3][1]
        triangle.vec_2.z = vector.x * projection_matrix.matrix[0][2] + vector.y * projection_matrix.matrix[1][2] + vector.z * projection_matrix.matrix[2][2] + projection_matrix.matrix[3][2]
        w = vector.x * projection_matrix.matrix[0][3] + vector.y * projection_matrix.matrix[1][3] + vector.z * projection_matrix.matrix[2][3] + projection_matrix.matrix[3][3]

        if w != 0:
            triangle.vec_2.x /= w
            triangle.vec_2.y /= w
            triangle.vec_2.z /= w
    
    else:
        triangle.vec_3.x = vector.x * projection_matrix.matrix[0][0] + vector.y * projection_matrix.matrix[1][0] + vector.z * projection_matrix.matrix[2][0] + projection_matrix.matrix[3][0]
        triangle.vec_3.y = vector.x * projection_matrix.matrix[0][1] + vector.y * projection_matrix.matrix[1][1] + vector.z * projection_matrix.matrix[2][1] + projection_matrix.matrix[3][1]
        triangle.vec_3.z = vector.x * projection_matrix.matrix[0][2] + vector.y * projection_matrix.matrix[1][2] + vector.z * projection_matrix.matrix[2][2] + projection_matrix.matrix[3][2]
        w = vector.x * projection_matrix.matrix[0][3] + vector.y * projection_matrix.matrix[1][3] + vector.z * projection_matrix.matrix[2][3] + projection_matrix.matrix[3][3]

        if w != 0:
            triangle.vec_3.x /= w
            triangle.vec_3.y /= w
            triangle.vec_3.z /= w

def get_color(lum):
    '''Converts an illumaned value to greyscale ASCII'''
    pixel_bw = int(4 * lum)
    if pixel_bw == 0:
        return u'\u2591'
    if pixel_bw == 1:
        return u'\u2592'
    if pixel_bw == 2:
        return u'\u2593'
    if pixel_bw >= 3:
        return u'\u2588'


if __name__ == '__main__':

    CMD_FONT = 5            # Console ASCII font size
    SCREEN_WIDTH = 256      # Console Screen Size X (columns)
    SCREEN_HEIGHT = 127     # Console Screen Size Y (rows)

    cmd_engine = ConsoleRenderEngine(CMD_FONT, SCREEN_WIDTH, SCREEN_HEIGHT)


    # Initiate time variables for rotating mesh
    tp1 = time.perf_counter()
    tp2 = time.perf_counter()
    THETA = 0

    # Initiate world classes
    camera = Vector()
    mesh = CubeMesh()

    # Simulation loop
    while 1:

        # Reset screen
        cmd_engine.reset_screen()

        # Quit simulation
        if keyboard.is_pressed('Q'):
            cmd_engine.on_user_destroy()
            sys.exit()

        # Rotation projection matrices
        mat_rot_z = ProjectionMatrix()
        mat_rot_x = ProjectionMatrix()

        # Calculate time differential per frame
        tp2 = time.perf_counter()
        elapsed_time = tp2 - tp1
        tp1 = tp2
        THETA += 1 * elapsed_time

        # Rotation Z projection matrix
        mat_rot_z.matrix[0][0] = math.cos(THETA)
        mat_rot_z.matrix[0][1] = math.sin(THETA)
        mat_rot_z.matrix[1][0] = -math.sin(THETA)
        mat_rot_z.matrix[1][1] = math.cos(THETA)
        mat_rot_z.matrix[2][2] = 1
        mat_rot_z.matrix[3][3] = 1

        # Rotation X projection matrix
        mat_rot_x.matrix[0][0] = 1
        mat_rot_x.matrix[1][1] = math.cos(THETA * 0.5)
        mat_rot_x.matrix[1][2] = math.sin(THETA * 0.5)
        mat_rot_x.matrix[2][1] = -math.sin(THETA * 0.5)
        mat_rot_x.matrix[2][2] = math.cos(THETA * 0.5)
        mat_rot_x.matrix[3][3] = 1

        # Mech projection matrix
        NEAR = 0.1
        FAR = 1000
        FOV = 90
        ASPECT_RATIO = SCREEN_HEIGHT / SCREEN_WIDTH
        FOV_RAD = 1 / math.atan(FOV * 0.5 / 180 * 3.14159)

        matrix_prog = ProjectionMatrix()
        matrix_prog.matrix[0][0] = ASPECT_RATIO * FOV_RAD
        matrix_prog.matrix[1][1] = FOV_RAD
        matrix_prog.matrix[2][2] = FAR / (FAR - NEAR)
        matrix_prog.matrix[3][2] = (-FAR * NEAR) / (FAR - NEAR)
        matrix_prog.matrix[2][3] = 1
        matrix_prog.matrix[3][3] = 0

        # Holds triangles for sorting
        vec_triangles_to_raster = []

        # Iterate through predefined triangles
        for tri in mesh.tris:
            # Initiate output projected triangle
            tri_projected = Triangle(Vector(), Vector(), Vector())
            tri_rotated_z = Triangle(Vector(), Vector(), Vector())
            tri_rotated_zx = Triangle(Vector(), Vector(), Vector())

            # Rotate Z
            multiply_matrix_vector(tri.vec_1, tri_rotated_z, 1, mat_rot_z)
            multiply_matrix_vector(tri.vec_2, tri_rotated_z, 2, mat_rot_z)
            multiply_matrix_vector(tri.vec_3, tri_rotated_z, 3, mat_rot_z)

            # Rotate X
            multiply_matrix_vector(tri_rotated_z.vec_1, tri_rotated_zx, 1, mat_rot_x)
            multiply_matrix_vector(tri_rotated_z.vec_2, tri_rotated_zx, 2, mat_rot_x)
            multiply_matrix_vector(tri_rotated_z.vec_3, tri_rotated_zx, 3, mat_rot_x)

            # Offset triangle into the screen
            tri_translated = Triangle(Vector(tri_rotated_zx.vec_1.x, tri_rotated_zx.vec_1.y, tri_rotated_zx.vec_1.z),
                                      Vector(tri_rotated_zx.vec_2.x, tri_rotated_zx.vec_2.y, tri_rotated_zx.vec_2.z),
                                      Vector(tri_rotated_zx.vec_3.x, tri_rotated_zx.vec_3.y, tri_rotated_zx.vec_3.z))

            tri_translated.vec_1.z = tri_rotated_zx.vec_1.z + 3
            tri_translated.vec_2.z = tri_rotated_zx.vec_2.z + 3
            tri_translated.vec_3.z = tri_rotated_zx.vec_3.z + 3

            # Calculate triangle normals
            normal, line1, line2 = Vector(), Vector(), Vector()
            line1.x = tri_translated.vec_2.x - tri_translated.vec_1.x
            line1.y = tri_translated.vec_2.y - tri_translated.vec_1.y
            line1.z = tri_translated.vec_2.z - tri_translated.vec_1.z

            line2.x = tri_translated.vec_3.x - tri_translated.vec_1.x
            line2.y = tri_translated.vec_3.y - tri_translated.vec_1.y
            line2.z = tri_translated.vec_3.z - tri_translated.vec_1.z

            normal.x = line1.y * line2.z - line1.z * line2.y
            normal.y = line1.z * line2.x - line1.x * line2.z
            normal.z = line1.x * line2.y - line1.y * line2.x

            l = math.sqrt(normal.x * normal.x + normal.y * normal.y + normal.z * normal.z)
            normal.x /= l
            normal.y /= l
            normal.z /= l

            if (normal.x * (tri_translated.vec_1.x - camera.x) +
                normal.y * (tri_translated.vec_1.y - camera.y) +
                normal.z * (tri_translated.vec_1.z - camera.z) < 0):

                # Calculate illumination
                light_direction = Vector(0, 0, -1)
                l = math.sqrt(light_direction.x * light_direction.x +
                              light_direction.y * light_direction.y +
                              light_direction.z * light_direction.z)
                light_direction.x /= l
                light_direction.y /= l
                light_direction.z /= l

                # Calculate dot product of triangle normal and light direction
                dp = (normal.x * light_direction.x +
                      normal.y * light_direction.y +
                      normal.z * light_direction.z)

                # Set symbol in triangle
                tri_translated.char = get_color(dp)

                # Calculate projected triangle vlaues
                multiply_matrix_vector(tri_translated.vec_1, tri_projected, 1, matrix_prog)
                multiply_matrix_vector(tri_translated.vec_2, tri_projected, 2, matrix_prog)
                multiply_matrix_vector(tri_translated.vec_3, tri_projected, 3, matrix_prog)
                tri_projected.char = tri_translated.char

                # Scale into view
                tri_projected.vec_1.x += 1
                tri_projected.vec_1.y += 1
                tri_projected.vec_2.x += 1
                tri_projected.vec_2.y += 1
                tri_projected.vec_3.x += 1
                tri_projected.vec_3.y += 1
                tri_projected.vec_1.x *= 0.5 * SCREEN_WIDTH
                tri_projected.vec_1.y *= 0.5 * SCREEN_HEIGHT
                tri_projected.vec_2.x *= 0.5 * SCREEN_WIDTH
                tri_projected.vec_2.y *= 0.5 * SCREEN_HEIGHT
                tri_projected.vec_3.x *= 0.5 * SCREEN_WIDTH
                tri_projected.vec_3.y *= 0.5 * SCREEN_HEIGHT

                vec_triangles_to_raster.append(tri_projected)

        # Sort triangles from back to front "painters algorithm"
        vec_triangles_to_raster.sort(key=lambda tri:
                                    (tri.vec_1.z + tri.vec_2.z + tri.vec_3.z) / 3, reverse=True)

        for tri_projected in vec_triangles_to_raster:

            # Fill in triangles to cmd engine screen
            cmd_engine.fill_triangle(int(tri_projected.vec_1.x), int(tri_projected.vec_1.y),
                                    int(tri_projected.vec_2.x), int(tri_projected.vec_2.y),
                                    int(tri_projected.vec_3.x), int(tri_projected.vec_3.y),
                                    tri_projected.char)

            # Draw wireframe lines to cmd engine screen
            cmd_engine.draw_triangle(int(tri_projected.vec_1.x), int(tri_projected.vec_1.y),
                                    int(tri_projected.vec_2.x), int(tri_projected.vec_2.y),
                                    int(tri_projected.vec_3.x), int(tri_projected.vec_3.y),
                                    ' ')

        # Render current screen to command
        cmd_engine.display_screen()
