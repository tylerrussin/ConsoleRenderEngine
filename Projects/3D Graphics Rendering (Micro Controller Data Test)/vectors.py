'''Class for preforming calculation with vectors'''
import math
from dataclasses import dataclass


@dataclass
class Vector:
    '''Holds 3D vector coordinates'''

    x: int = 0
    y: int = 0
    z: int = 0
    w: int = 1


def add(vec_1: Vector, vec_2: Vector) -> Vector:
    '''Add two vectors into new vector'''
    return Vector(vec_1.x + vec_2.x, vec_1.y + vec_2.y, vec_1.z + vec_2.z)

def subtract(vec_1: Vector, vec_2: Vector) -> Vector:
    '''Subtract two vectors into new vector'''
    return Vector(vec_1.x - vec_2.x, vec_1.y - vec_2.y, vec_1.z - vec_2.z)

def multiply(vec_1: Vector, k: int) -> Vector:
    '''Multiply vector and constant into new vector'''
    return Vector(vec_1.x * k, vec_1.y * k, vec_1.z * k)

def divide(vec_1: Vector, k: int) -> Vector:
    '''Divide vector and constant into new vector'''
    return Vector(vec_1.x / k, vec_1.y / k, vec_1.z / k)

def dot_product(vec_1: Vector, vec_2: Vector) -> int:
    '''Calculate and return dot product of two vectors'''
    return vec_1.x * vec_2.x + vec_1.y * vec_2.y + vec_1.z * vec_2.z

def length(vec_1: Vector) -> int:
    '''Calculate and return a vector length'''
    return math.sqrt(dot_product(vec_1, vec_1))

def normalize(vec_1: Vector) -> Vector:
    '''Normilize vector into new vector'''
    l = length(vec_1)
    if l == 0:
        l += 0.001
    return Vector(vec_1.x / l, vec_1.y / l, vec_1.z / l)

def cross_product(vec_1: Vector, vec_2: Vector) -> Vector:
    '''Calculate cross product of two vectors into new vector'''
    vec_3 = Vector()
    vec_3.x = vec_1.y * vec_2.z - vec_1.z * vec_2.y
    vec_3.y = vec_1.z * vec_2.x - vec_1.x * vec_2.z
    vec_3.z = vec_1.x * vec_2.y - vec_1.y * vec_2.x
    return vec_3

def intersect_plane(plane_point: Vector, plane_normal: Vector,
                    line_start: Vector, line_end: Vector) -> Vector:
    '''Test and return a vector where a given line intersects with a given plane'''

    # Line intersect with plane algorithm
    plane_normal = normalize(plane_normal)
    plane_d = -dot_product(plane_normal, plane_point)

    ad = dot_product(line_start, plane_normal)
    bd = dot_product(line_end, plane_normal)
    t = (-plane_d - ad) / (bd - ad)

    line_start_to_end = subtract(line_end, line_start)
    line_to_intersect = multiply(line_start_to_end, t)

    return add(line_start, line_to_intersect)

def multiply_matrix_vector(mat: list[list[int]], i: Vector) -> Vector:
    '''Calculate a projected verison of a vector into a new vector'''
    vec_1 = Vector()
    vec_1.x = i.x * mat.m[0][0] + i.y * mat.m[1][0] + i.z * mat.m[2][0] + i.w * mat.m[3][0]
    vec_1.y = i.x * mat.m[0][1] + i.y * mat.m[1][1] + i.z * mat.m[2][1] + i.w * mat.m[3][1]
    vec_1.z = i.x * mat.m[0][2] + i.y * mat.m[1][2] + i.z * mat.m[2][2] + i.w * mat.m[3][2]
    vec_1.w = i.x * mat.m[0][3] + i.y * mat.m[1][3] + i.z * mat.m[2][3] + i.w * mat.m[3][3]
    return vec_1
