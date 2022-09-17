'''Graphical Rendering in The Command Line'''

import os
import sys
import math
import time

import keyboard

# Path restructure for imports
script_dir = os.path.dirname( __file__ )
main_dir = os.path.join( script_dir, '../..' )
sys.path.append( main_dir )

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

    @staticmethod
    def intersect_plane(plane_p: Vector, plane_n: Vector, line_start: Vector, line_end: Vector) -> Vector:

        plane_n = VectorMath.normalize(plane_n)
        plane_d = -VectorMath.dot_product(plane_n, plane_p)
        ad = VectorMath.dot_product(line_start, plane_n)
        bd = VectorMath.dot_product(line_end, plane_n)
        t = (-plane_d - ad) / (bd - ad)
        lineStartToEnd = VectorMath.subtract(line_end, line_start)
        lineToIntersect = VectorMath.multiply(lineStartToEnd, t)
        return VectorMath.add(line_start, lineToIntersect)


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

    @staticmethod
    def point_at(pos: Vector, target: Vector, up: Vector) -> ProjectionMatrix:

        # Calculate new forward direction
        new_forward = VectorMath.subtract(target, pos)
        new_forward = VectorMath.normalize(new_forward)

        # Calculate new up direction
        a = VectorMath.multiply(new_forward, VectorMath.dot_product(up, new_forward))
        new_up = VectorMath.subtract(up, a)
        new_up = VectorMath.normalize(new_up)

        # New right direction is easy, its just the cross product
        new_right = VectorMath.cross_product(new_up, new_forward)

        # Construct dimensioning and translation matrix
        matrix = ProjectionMatrix()
        matrix.m[0][0] = new_right.x
        matrix.m[0][1] = new_right.y
        matrix.m[0][2] = new_right.z
        matrix.m[0][3] = 0

        matrix.m[1][0] = new_up.x
        matrix.m[1][1] = new_up.y
        matrix.m[1][2] = new_up.z
        matrix.m[1][3] = 0

        matrix.m[2][0] = new_forward.x
        matrix.m[2][1] = new_forward.y
        matrix.m[2][2] = new_forward.z
        matrix.m[2][3] = 0

        matrix.m[3][0] = pos.x
        matrix.m[3][1] = pos.y
        matrix.m[3][2] = pos.z
        matrix.m[3][3] = 1

        return matrix

    @staticmethod
    def quick_inverse(m: ProjectionMatrix) -> ProjectionMatrix: # Only for Rotation/Tranlation Matrices
        matrix = ProjectionMatrix()
        
        matrix.m[0][0] = m.m[0][0]
        matrix.m[0][1] = m.m[1][0]
        matrix.m[0][2] = m.m[2][0]
        matrix.m[0][3] = 0

        matrix.m[1][0] = m.m[0][1]
        matrix.m[1][1] = m.m[1][1]
        matrix.m[1][2] = m.m[2][1]
        matrix.m[1][3] = 0

        matrix.m[2][0] = m.m[0][2]
        matrix.m[2][1] = m.m[1][2]
        matrix.m[2][2] = m.m[2][2]
        matrix.m[2][3] = 0

        matrix.m[3][0] = -(m.m[3][0] * matrix.m[0][0] + m.m[3][1] * matrix.m[1][0] + m.m[3][2] * matrix.m[2][0])
        matrix.m[3][1] = -(m.m[3][0] * matrix.m[0][1] + m.m[3][1] * matrix.m[1][1] + m.m[3][2] * matrix.m[2][1])
        matrix.m[3][2] = -(m.m[3][0] * matrix.m[0][2] + m.m[3][1] * matrix.m[1][2] + m.m[3][2] * matrix.m[2][2])
        matrix.m[3][3] = 1
        
        return matrix

def auto_dist(p: Vector, plane_n, plane_p) -> Vector:
    n = VectorMath.normalize(p)
    return plane_n.x * p.x + plane_n.y * p.y + plane_n.z * p.z - VectorMath.dot_product(plane_n, plane_p)

def triangle_clip_against_plane(plane_p: Vector, plane_n:Vector, in_tri: Triangle, out_tris: list) -> int:


    # Make sure plane normal is indeed normal
    plane_n = VectorMath.normalize(plane_n)

    # Return signed shortest distance from point to plane, plane normal must be normalised
    # auto_dist

    # Create two temporary storage arrays to classify points either side of plane
    # If distance sign is positive, point lies on "inside" of plane
    inside_points = [Vector(), Vector(), Vector()]
    inside_point_count = 0
    outside_points = [Vector(), Vector(), Vector()]
    outside_point_count = 0

    # Get signed distance of each point in triangle to plane
    d0 = auto_dist(in_tri.vec_1, plane_n, plane_p)
    d1 = auto_dist(in_tri.vec_2, plane_n, plane_p)
    d2 = auto_dist(in_tri.vec_3, plane_n, plane_p)

    if d0 >= 0:
        
        inside_points[inside_point_count] = in_tri.vec_1
        inside_point_count += 1
    else:
        
        outside_points[outside_point_count] = in_tri.vec_1
        outside_point_count += 1

    if d1 >= 0:
        
        inside_points[inside_point_count] = in_tri.vec_2
        inside_point_count += 1
    else:
        
        outside_points[outside_point_count] = in_tri.vec_2
        outside_point_count += 1

    if d2 >= 0:
        
        inside_points[inside_point_count] = in_tri.vec_3
        inside_point_count += 1
    else:
        
        outside_points[outside_point_count] = in_tri.vec_3
        outside_point_count += 1

    # Now classify triangle points, and break the input triangle into 
    # smaller output triangles if required. There are four possible
    # outcomes...

    if inside_point_count == 0:

        # All points lie on the outside of plane, so clip whole triangle
        # It ceases to exist

        return 0 # No returned triangles are valid

    if inside_point_count == 3:

        # All points lie on the inside of plane, so do nothing
        # and allow the triangle to simply pass through
        out_tris[0].vec_1 = in_tri.vec_1
        out_tris[0].vec_2 = in_tri.vec_2
        out_tris[0].vec_3 = in_tri.vec_3

                # Copy appearance info to new triangle
        out_tris[0].col =  in_tri.col
        out_tris[0].sym = in_tri.sym

        return 1 # Just the one returned original triangle is valid


    if inside_point_count == 1 and outside_point_count == 2:

        # Triangle should be clipped. As two points lie outside
        # the plane, the triangle simply becomes a smaller triangle

        # Copy appearance info to new triangle
        out_tris[0].col = in_tri.col
        out_tris[0].sym = in_tri.sym

        # The inside point is valid, so keep that...
        out_tris[0].vec_1 = inside_points[0]

        # but the two new points are at the locations where the 
        # original sides of the triangle (lines) intersect with the plane
        out_tris[0].vec_2 = VectorMath.intersect_plane(plane_p, plane_n, inside_points[0], outside_points[0])
        out_tris[0].vec_3 = VectorMath.intersect_plane(plane_p, plane_n, inside_points[0], outside_points[1])

        return 1 # Return the newly formed single triangle


    if inside_point_count == 2 and outside_point_count == 1:

        # Triangle should be clipped. As two points lie inside the plane,
        # the clipped triangle becomes a "quad". Fortunately, we can
        # represent a quad with two new triangles

        # Copy appearance info to new triangles
        out_tris[0].col = in_tri.col
        out_tris[0].sym = in_tri.sym

        out_tris[1].col =  in_tri.col
        out_tris[1].sym = in_tri.sym

        # The first triangle consists of the two inside points and a new
        # point determined by the location where one side of the triangle
        # intersects with the plane
        out_tris[0].vec_1 = inside_points[0]
        out_tris[0].vec_2 = inside_points[1]
        out_tris[0].vec_3 = VectorMath.intersect_plane(plane_p, plane_n, inside_points[0], outside_points[0])

        # The second triangle is composed of one of he inside points, a
        # new point determined by the intersection of the other side of the 
        # triangle and the plane, and the newly created point above
        out_tris[1].vec_1 = inside_points[1]
        out_tris[1].vec_2 = out_tris[0].vec_3
        out_tris[1].vec_3 = VectorMath.intersect_plane(plane_p, plane_n, inside_points[1], outside_points[0])

        return 2 # Return two newly formed triangles which form a quad



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
    v_camera = Vector()
    v_look_dir = Vector()
    yaw = 0

    mesh = CubeMesh()
    mesh = Mesh('data/groot.obj')

    matrix_prog = MatrixMath.make_projection(90, SCREEN_HEIGHT / SCREEN_WIDTH, 0.1, 1000)

    # Simulation loop
    while 1:

        # Reset screen
        cmd_engine.reset_screen()

        # Quit simulation
        if keyboard.is_pressed('P'):
            cmd_engine.on_user_destroy()
            sys.exit()

        # Calculate time differential per frame
        tp2 = time.perf_counter()
        elapsed_time = tp2 - tp1
        tp1 = tp2
        # THETA += 1 * elapsed_time

        # Move v_camera
        if keyboard.is_pressed('UP_ARROW'):
            v_camera.y += 8 * elapsed_time

        # Move v_camera
        if keyboard.is_pressed('DOWN_ARROW'):
            v_camera.y -= 8 * elapsed_time

        # Move v_camera
        if keyboard.is_pressed('LEFT_ARROW'):
            v_camera.x += 8 * elapsed_time

        # Move v_camera
        if keyboard.is_pressed('RIGHT_ARROW'):
            v_camera.x -= 8 * elapsed_time

        v_forward = VectorMath.multiply(v_look_dir, 8 * elapsed_time)

        # Move yaw
        if keyboard.is_pressed('W'):
            v_camera = VectorMath.add(v_camera, v_forward)
        # Move yaw
        if keyboard.is_pressed('S'):
            v_camera = VectorMath.subtract(v_camera, v_forward)

        # Move yaw
        if keyboard.is_pressed('A'):
            yaw -= 2 * elapsed_time
        # Move yaw
        if keyboard.is_pressed('D'):
            yaw += 2 * elapsed_time



        # Rotation Z projection matrix
        mat_rot_z = MatrixMath.make_rotation_z(THETA)

        # Rotation X projection matrix
        mat_rot_x = MatrixMath.make_rotation_x(THETA * 0.5)

        # Correct distance to see cube
        mat_trans = MatrixMath.make_translation(0, 0, 16)

        mat_world = MatrixMath.make_identity()    # Form World Matrix
        mat_world = MatrixMath.multiply_matrix(mat_rot_z, mat_rot_x) # Transform by rotation
        mat_world = MatrixMath.multiply_matrix(mat_world, mat_trans) # Transform by translation

        v_up = Vector(0, 1, 0)
        v_target = Vector(0, 0, 1)
        mat_camera_rot = MatrixMath.make_rotation_y(yaw)
        v_look_dir = VectorMath.multiply_matrix_vector(mat_camera_rot, v_target)
        v_target = VectorMath.add(v_camera, v_look_dir)


        mat_camera = MatrixMath.point_at(v_camera, v_target, v_up)
        mat_view = MatrixMath.quick_inverse(mat_camera)


        # Holds triangles for sorting
        vec_triangles_to_raster = []

        # Iterate through predefined triangles
        for tri in mesh.tris:
            # Initiate output projected triangle
            tri_projected = Triangle(Vector(), Vector(), Vector())
            tri_transformed = Triangle(Vector(), Vector(), Vector())
            tri_viewed = Triangle(Vector(), Vector(), Vector())

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
            vCameraRay = VectorMath.subtract(tri_transformed.vec_1, v_camera)

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

                # Convert World Space --> View Space
                tri_viewed.vec_1 = VectorMath.multiply_matrix_vector(mat_view, tri_transformed.vec_1)
                tri_viewed.vec_2 = VectorMath.multiply_matrix_vector(mat_view, tri_transformed.vec_2)
                tri_viewed.vec_3 = VectorMath.multiply_matrix_vector(mat_view, tri_transformed.vec_3)
                tri_viewed.sym = tri_transformed.sym
                tri_viewed.col = tri_transformed.col

                # Clip Viewed Triangle against near plane, this could form two additional
                # additional triangles. 
                clipped_triangles = 0
                clipped = [Triangle(Vector(), Vector(), Vector()), Triangle(Vector(), Vector(), Vector())]
                clipped_triangles = triangle_clip_against_plane(Vector(0,0,0.5), Vector(0,0,1), tri_viewed, clipped)


                for n in range(0, clipped_triangles):

                    # Project triangles from 3D -> 2D
                    tri_projected.vec_1 = VectorMath.multiply_matrix_vector(matrix_prog, clipped[n].vec_1)
                    tri_projected.vec_2 = VectorMath.multiply_matrix_vector(matrix_prog, clipped[n].vec_2)
                    tri_projected.vec_3 = VectorMath.multiply_matrix_vector(matrix_prog, clipped[n].vec_3)
                    tri_projected.sym = clipped[n].sym
                    tri_projected.col = clipped[n].col

                    # Normilize
                    tri_projected.vec_1 = VectorMath.divide(tri_projected.vec_1, tri_projected.vec_1.w)
                    tri_projected.vec_2 = VectorMath.divide(tri_projected.vec_2, tri_projected.vec_2.w)
                    tri_projected.vec_3 = VectorMath.divide(tri_projected.vec_3, tri_projected.vec_3.w)

                    # X/Y are inverted so put them back
                    tri_projected.vec_1.x *= -1
                    tri_projected.vec_2.x *= -1
                    tri_projected.vec_3.x *= -1
                    tri_projected.vec_1.y *= -1
                    tri_projected.vec_2.y *= -1
                    tri_projected.vec_3.y *= -1

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

                    # overwritting problem when two triangles renered
                    test = Triangle(Vector(), Vector(), Vector())
                    test.vec_1 = tri_projected.vec_1
                    test.vec_2 = tri_projected.vec_2
                    test.vec_3 = tri_projected.vec_3
                    test.sym = tri_projected.sym
                    test.col = tri_projected.col
                    vec_triangles_to_raster.append(test)

        # Sort triangles from back to front "painters algorithm"
        vec_triangles_to_raster.sort(key=lambda tri:
                                    (tri.vec_1.z + tri.vec_2.z + tri.vec_3.z) / 3, reverse=True)

        for tri_to_rastor in vec_triangles_to_raster:

            # Clip triangles against all four screen edges, this could yield
            # a bunch of triangles, so create a queue that we traverse to 
            #  ensure we only test new triangles generated against planes
            clipped = [Triangle(Vector(), Vector(), Vector()), Triangle(Vector(), Vector(), Vector())]
            list_triangles = []

            # Add initial triangle
            list_triangles.append(tri_to_rastor)
            new_triangles = 1

            for p in range(0, 4):
            
                tris_to_add = 0
                while new_triangles > 0:
                
                    # Take triangle from front of queue
                    test = list_triangles.pop(0)
                    new_triangles -= 1

                    # Clip it against a plane. We only need to test each 
                    # subsequent plane, against subsequent new triangles
                    # as all triangles after a plane clip are guaranteed
                    # to lie on the inside of the plane. I like how this
                    # comment is almost completely and utterly justified
                    if p == 0:	
                        tris_to_add = triangle_clip_against_plane(Vector(0,0,0), Vector(0,1,0), test, clipped)
                        
                    elif p == 1:
                        tris_to_add = triangle_clip_against_plane(Vector(0, SCREEN_HEIGHT - 1, 0), Vector(0, -1, 0), test, clipped)
                        
                    elif p == 2:
                        tris_to_add = triangle_clip_against_plane(Vector(0,0,0), Vector(1,0,0), test, clipped)
                        
                    elif p == 3:
                        tris_to_add = triangle_clip_against_plane(Vector(SCREEN_WIDTH - 1, 0, 0), Vector(-1,0,0), test, clipped)
                        
                

                    # Clipping may yield a variable number of triangles, so
                    # add these new ones to the back of the queue for subsequent
                    # clipping against next planes
                    for w in range(0, tris_to_add):

                        # overwritting problem when two triangles renered
                        test = Triangle(Vector(), Vector(), Vector())
                        test.vec_1 = clipped[w].vec_1
                        test.vec_2 = clipped[w].vec_2
                        test.vec_3 = clipped[w].vec_3
                        test.sym = clipped[w].sym
                        test.col = clipped[w].col
                        list_triangles.append(test)

                new_triangles = len(list_triangles)



            # Draw the transformed, viewed, clipped, projected, sorted, clipped triangles
            for t in list_triangles:

                # Fill in triangles to cmd engine screen
                cmd_engine.fill_triangle(int(t.vec_1.x), int(t.vec_1.y),
                                        int(t.vec_2.x), int(t.vec_2.y),
                                        int(t.vec_3.x), int(t.vec_3.y),
                                        t.sym, t.col)

                # # Draw wireframe lines to cmd engine screen
                # cmd_engine.draw_triangle(int(t.vec_1.x), int(t.vec_1.y),
                #                         int(t.vec_2.x), int(t.vec_2.y),
                #                         int(t.vec_3.x), int(t.vec_3.y),
                #                         PIXEL_SOLID, [FG_BLACK, BG_BLACK])



        # Render current screen to command
        cmd_engine.display_screen()


