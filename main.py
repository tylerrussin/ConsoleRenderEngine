'''Graphical Rendering in The Command Line'''

import sys
import math
import time

import keyboard

from console_render_engine import ConsoleRenderEngine
from mesh_classes import Vector, Triangle, ProjectionMatrix, CubeMesh, Mesh


class VectorMath:
    '''Math operations performed on 3D vectors'''

    @staticmethod
    def add(vec_1: Vector, vec_2: Vector) -> Vector:
        '''Add two vectors into new vector'''
        return Vector(vec_1.x + vec_2.x, vec_1.y + vec_2.y, vec_1.z + vec_2.z)

    @staticmethod
    def subtract(vec_1: Vector, vec_2: Vector) -> Vector:
        '''Subtract two vectors into new vector'''
        return Vector(vec_1.x - vec_2.x, vec_1.y - vec_2.y, vec_1.z - vec_2.z)

    @staticmethod
    def multiply(vec_1: Vector, k: int) -> Vector:
        '''Multiply vector and constant into new vector'''
        return Vector(vec_1.x * k, vec_1.y * k, vec_1.z * k)

    @staticmethod
    def divide(vec_1: Vector, k: int) -> Vector:
        '''Divide vector and constant into new vector'''
        return Vector(vec_1.x / k, vec_1.y / k, vec_1.z / k)

    @staticmethod
    def dot_product(vec_1: Vector, vec_2: Vector) -> int:
        '''Calculate and return dot product of two vectors'''
        return vec_1.x * vec_2.x + vec_1.y * vec_2.y + vec_1.z * vec_2.z

    @staticmethod
    def length(vec_1: Vector) -> int:
        '''Calculate and return a vector length'''
        return math.sqrt(VectorMath.dot_product(vec_1, vec_1))

    @staticmethod
    def normalize(vec_1: Vector) -> Vector:
        '''Normilize vector into new vector'''
        length = VectorMath.length(vec_1)
        return Vector(vec_1.x / length, vec_1.y / length, vec_1.z / length)

    @staticmethod
    def cross_product(vec_1: Vector, vec_2: Vector) -> Vector:
        '''Calculate cross product of two vectors into new vector'''
        vec_3 = Vector()
        vec_3.x = vec_1.y * vec_2.z - vec_1.z * vec_2.y
        vec_3.y = vec_1.z * vec_2.x - vec_1.x * vec_2.z
        vec_3.z = vec_1.x * vec_2.y - vec_1.y * vec_2.x
        return vec_3

    @staticmethod
    def multiply_matrix_vector(mat: ProjectionMatrix, i: Vector) -> Vector:
        '''Calculate a projected verison of a vector into a new vector'''
        vec_1 = Vector()
        vec_1.x = i.x * mat.m[0][0] + i.y * mat.m[1][0] + i.z * mat.m[2][0] + i.w * mat.m[3][0]
        vec_1.y = i.x * mat.m[0][1] + i.y * mat.m[1][1] + i.z * mat.m[2][1] + i.w * mat.m[3][1]
        vec_1.z = i.x * mat.m[0][2] + i.y * mat.m[1][2] + i.z * mat.m[2][2] + i.w * mat.m[3][2]
        vec_1.w = i.x * mat.m[0][3] + i.y * mat.m[1][3] + i.z * mat.m[2][3] + i.w * mat.m[3][3]
        return vec_1

class MatrixMath:
    '''Math operations preformed on projection matrices'''

    @staticmethod
    def make_identity() -> ProjectionMatrix:
        '''Initialize a projection matrix'''
        mat = ProjectionMatrix()
        mat.m[0][0] = 1
        mat.m[1][1] = 1
        mat.m[2][2] = 1
        mat.m[3][3] = 1
        return mat

    @staticmethod
    def make_rotation_x(angle_radian: float) -> ProjectionMatrix:
        '''Calculate a rotated projection matrix x based on radian'''
        mat = ProjectionMatrix()
        mat.m[0][0] = 1
        mat.m[1][1] = math.cos(angle_radian)
        mat.m[1][2] = math.sin(angle_radian)
        mat.m[2][1] = -math.sin(angle_radian)
        mat.m[2][2] = math.cos(angle_radian)
        mat.m[3][3] = 1
        return mat

    @staticmethod
    def make_rotation_y(angle_radian: float) -> ProjectionMatrix:
        '''Calculate a rotated projection matrix y based on radian'''
        mat = ProjectionMatrix()
        mat.m[0][0] = math.cos(angle_radian)
        mat.m[0][2] = math.sin(angle_radian)
        mat.m[2][0] = -math.sin(angle_radian)
        mat.m[1][1] = 1
        mat.m[2][2] = math.cos(angle_radian)
        mat.m[3][3] = 1
        return mat

    @staticmethod
    def make_rotation_z(angle_radian: float) -> ProjectionMatrix:
        '''Calculate a rotated projection matrix z based on radian'''
        mat = ProjectionMatrix()
        mat.m[0][0] = math.cos(angle_radian)
        mat.m[0][1] = math.sin(angle_radian)
        mat.m[1][0] = -math.sin(angle_radian)
        mat.m[1][1] = math.cos(angle_radian)
        mat.m[2][2] = 1
        mat.m[3][3] = 1
        return mat

    @staticmethod
    def make_translation(x: int, y: int, z: int) -> ProjectionMatrix:
        '''Calculate a translated projection matrix based on new coords'''
        mat = ProjectionMatrix()
        mat.m[0][0] = 1
        mat.m[1][1] = 1
        mat.m[2][2] = 1
        mat.m[3][3] = 1
        mat.m[3][0] = x
        mat.m[3][1] = y
        mat.m[3][2] = z
        return mat

    @staticmethod
    def make_projection(fov_degrees: float, aspect_ratio: float,
                        near: int, far: int) -> ProjectionMatrix:
        '''Calculate a projection matrix based on player view'''

        fov_radians = 1 / math.tan(fov_degrees * 0.5 / 180 * 3.14159)
        mat = ProjectionMatrix()
        mat.m[0][0] = aspect_ratio * fov_radians
        mat.m[1][1] = fov_radians
        mat.m[2][2] = far / (far - near)
        mat.m[3][2] = (-far * near) / (far - near)
        mat.m[2][3] = 1
        mat.m[3][3] = 0
        return mat

    @staticmethod
    def multiply_matrix(m_1: ProjectionMatrix, m_2: ProjectionMatrix) -> ProjectionMatrix:
        '''Multiply two projection matrices together'''
        mat = ProjectionMatrix()
        for col in range(0, 4):
            for row in range(0, 4):
                mat.m[row][col] = (m_1.m[row][0] * m_2.m[0][col] +
                                   m_1.m[row][1] * m_2.m[1][col] +
                                   m_1.m[row][2] * m_2.m[2][col] +
                                   m_1.m[row][3] * m_2.m[3][col])
        return mat


PIXEL_SOLID = '\u2588'
PIXEL_THREEQUARTERS = '\u2593'
PIXEL_HALF = '\u2592'
PIXEL_QUARTER = '\u2591'

FG_BLACK		= 0x0000
FG_DARK_BLUE    = 0x0001
FG_DARK_GREEN   = 0x0002
FG_DARK_CYAN    = 0x0003
FG_DARK_RED     = 0x0004
FG_DARK_MAGENTA = 0x0005
FG_DARK_YELLOW  = 0x0006
FG_GREY			= 0x0007
FG_DARK_GREY    = 0x0008
FG_BLUE			= 0x0009
FG_GREEN		= 0x000A
FG_CYAN			= 0x000B
FG_RED			= 0x000C
FG_MAGENTA		= 0x000D
FG_YELLOW		= 0x000E
FG_WHITE		= 0x000F
BG_BLACK		= 0x0000
BG_DARK_BLUE	= 0x0010
BG_DARK_GREEN	= 0x0020
BG_DARK_CYAN	= 0x0030
BG_DARK_RED		= 0x0040
BG_DARK_MAGENTA = 0x0050
BG_DARK_YELLOW	= 0x0060
BG_GREY			= 0x0070
BG_DARK_GREY	= 0x0080
BG_BLUE			= 0x0090
BG_GREEN		= 0x00A0
BG_CYAN			= 0x00B0
BG_RED			= 0x00C0
BG_MAGENTA		= 0x00D0
BG_YELLOW		= 0x00E0
BG_WHITE		= 0x00F0

def get_color(lum):
    '''Converts an illumaned value to greyscale ASCII'''
    pixel_bw = int(13 * lum)

    if pixel_bw == 0:
        bg_col = BG_BLACK 
        fg_col = FG_BLACK
        sym = PIXEL_SOLID
    elif pixel_bw == 1:
        bg_col = BG_BLACK 
        fg_col = FG_DARK_GREY
        sym = PIXEL_QUARTER
    elif pixel_bw == 2:
        bg_col = BG_BLACK 
        fg_col = FG_DARK_GREY
        sym = PIXEL_HALF
    elif pixel_bw == 3:
        bg_col = BG_BLACK 
        fg_col = FG_DARK_GREY
        sym = PIXEL_THREEQUARTERS
    elif pixel_bw == 4:
        bg_col = BG_BLACK 
        fg_col = FG_DARK_GREY
        sym = PIXEL_SOLID
    elif pixel_bw == 5:
        bg_col = BG_DARK_GREY 
        fg_col = FG_GREY
        sym = PIXEL_QUARTER
    elif pixel_bw == 6:
        bg_col = BG_DARK_GREY 
        fg_col = FG_GREY
        sym = PIXEL_HALF
    elif pixel_bw == 7:
        bg_col = BG_DARK_GREY 
        fg_col = FG_GREY
        sym = PIXEL_THREEQUARTERS
    elif pixel_bw == 8:
        bg_col = BG_DARK_GREY 
        fg_col = FG_GREY
        sym = PIXEL_SOLID
    elif pixel_bw == 9:
        bg_col = BG_GREY 
        fg_col = FG_WHITE
        sym = PIXEL_QUARTER
    elif pixel_bw == 10:
        bg_col = BG_GREY 
        fg_col = FG_WHITE
        sym = PIXEL_HALF
    elif pixel_bw == 11:
        bg_col = BG_GREY 
        fg_col = FG_WHITE
        sym = PIXEL_THREEQUARTERS
    elif pixel_bw == 12:
        bg_col = BG_GREY 
        fg_col = FG_WHITE
        sym = PIXEL_SOLID
    else:
        bg_col = BG_BLACK 
        fg_col = FG_BLACK
        sym = PIXEL_SOLID

    return [bg_col, fg_col], sym



if __name__ == '__main__':

    CMD_FONT = 5            # Console ASCII font size
    SCREEN_WIDTH = 256      # Console Screen Size X (columns)  #256#
    SCREEN_HEIGHT = 127     # Console Screen Size Y (rows)

    cmd_engine = ConsoleRenderEngine(CMD_FONT, SCREEN_WIDTH, SCREEN_HEIGHT)
    cmd_engine.on_user_create()

    # Initiate time variables for rotating mesh
    tp1 = time.perf_counter()
    tp2 = time.perf_counter()
    THETA = 0

    # Initiate world classes
    camera = Vector()
    mesh = CubeMesh()
    mesh = Mesh('data/axis.obj')

    matrix_prog = MatrixMath.make_projection(90, SCREEN_HEIGHT / SCREEN_WIDTH, 0.1, 1000)

    # Simulation loop
    while 1:

        # Reset screen
        cmd_engine.reset_screen()

        # Quit simulation
        if keyboard.is_pressed('Q'):
            cmd_engine.on_user_destroy()
            sys.exit()

        # Calculate time differential per frame
        tp2 = time.perf_counter()
        elapsed_time = tp2 - tp1
        tp1 = tp2
        THETA += 1 * elapsed_time

        # Rotation Z projection matrix
        mat_rot_z = MatrixMath.make_rotation_z(THETA)

        # Rotation X projection matrix
        mat_rot_x = MatrixMath.make_rotation_x(THETA * 0.5)

        # Correct distance to see cube
        mat_trans = MatrixMath.make_translation(0, 0, 16)

        mat_world = MatrixMath.make_identity()    # Form World Matrix
        mat_world = MatrixMath.multiply_matrix(mat_rot_z, mat_rot_x) # Transform by rotation
        mat_world = MatrixMath.multiply_matrix(mat_world, mat_trans) # Transform by translation


        # Holds triangles for sorting
        vec_triangles_to_raster = []

        # Iterate through predefined triangles
        for tri in mesh.tris:
            # Initiate output projected triangle
            tri_projected = Triangle(Vector(), Vector(), Vector())
            tri_transformed = Triangle(Vector(), Vector(), Vector())

            # World Matrix Transform
            tri_transformed.vec_1 = VectorMath.multiply_matrix_vector(mat_world, tri.vec_1)
            tri_transformed.vec_2 = VectorMath.multiply_matrix_vector(mat_world, tri.vec_2)
            tri_transformed.vec_3 = VectorMath.multiply_matrix_vector(mat_world, tri.vec_3)


            # Calculate triangle Normal

            # Get lines either side of triangle
            line1 = VectorMath.subtract(tri_transformed.vec_2, tri_transformed.vec_1)
            line2 = VectorMath.subtract(tri_transformed.vec_3, tri_transformed.vec_1)


            # Take cross product of lines to get normal to triangle surface
            normal = VectorMath.cross_product(line1, line2)

            # You normally need to normalise a normal!
            normal = VectorMath.normalize(normal)

            # Get Ray from triangle to camera
            vCameraRay = VectorMath.subtract(tri_transformed.vec_1, camera)

            # If ray is aligned with normal, then triangle is visible
            if VectorMath.dot_product(normal, vCameraRay) < 0:

                # Illumination
                light_direction = Vector(0, 1, -1)
                light_direction = VectorMath.normalize(light_direction)

                # Calculate dot product of triangle normal and light direction
                # How "aligned" are light direction and triangle surface normal?
                dp = max(0.1, VectorMath.dot_product(light_direction, normal))

                # Set symbol in triangle
                col, sym = get_color(dp)
                tri_transformed.col = col
                tri_transformed.sym = sym

                # Project triangles from 3D -> 2D
                tri_projected.vec_1 = VectorMath.multiply_matrix_vector(matrix_prog, tri_transformed.vec_1)
                tri_projected.vec_2 = VectorMath.multiply_matrix_vector(matrix_prog, tri_transformed.vec_2)
                tri_projected.vec_3 = VectorMath.multiply_matrix_vector(matrix_prog, tri_transformed.vec_3)
                tri_projected.sym = tri_transformed.sym
                tri_projected.col = tri_transformed.col

                # Normilize
                tri_projected.vec_1 = VectorMath.divide(tri_projected.vec_1, tri_projected.vec_1.w)
                tri_projected.vec_2 = VectorMath.divide(tri_projected.vec_2, tri_projected.vec_2.w)
                tri_projected.vec_3 = VectorMath.divide(tri_projected.vec_3, tri_projected.vec_3.w)

                # Scale into view
                vOffsetView = Vector(1, 1, 0)
                tri_projected.vec_1 = VectorMath.add(tri_projected.vec_1, vOffsetView)
                tri_projected.vec_2 = VectorMath.add(tri_projected.vec_2, vOffsetView)
                tri_projected.vec_3 = VectorMath.add(tri_projected.vec_3, vOffsetView)
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
                                    tri_projected.sym, tri_projected.col)

            # # Draw wireframe lines to cmd engine screen
            # cmd_engine.draw_triangle(int(tri_projected.vec_1.x), int(tri_projected.vec_1.y),
            #                         int(tri_projected.vec_2.x), int(tri_projected.vec_2.y),
            #                         int(tri_projected.vec_3.x), int(tri_projected.vec_3.y),
            #                         ' ')

        # Render current screen to command
        cmd_engine.display_screen()
