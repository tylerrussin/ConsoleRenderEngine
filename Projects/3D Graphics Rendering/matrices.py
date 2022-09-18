'''Class for preforming calculation with matrices'''
import math
from dataclasses import dataclass, field


@dataclass
class ProjectionMatrix:
    '''Holds projected matrix values'''

    m: list[list[int]] = field(default_factory=lambda:
                               [[0 for _ in range(4)] for y in range(4)])


def make_identity() -> ProjectionMatrix:
    '''Initialize a projection matrix'''
    mat = ProjectionMatrix()
    mat.m[0][0] = 1
    mat.m[1][1] = 1
    mat.m[2][2] = 1
    mat.m[3][3] = 1
    return mat

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

def multiply_matrix(m_1: ProjectionMatrix, m_2: ProjectionMatrix) -> ProjectionMatrix:
    '''Multiply two projection matrices together'''
    mat = ProjectionMatrix()
    for column in range(0, 4):
        for row in range(0, 4):
            mat.m[row][column] = (m_1.m[row][0] * m_2.m[0][column] +
                                    m_1.m[row][1] * m_2.m[1][column] +
                                    m_1.m[row][2] * m_2.m[2][column] +
                                    m_1.m[row][3] * m_2.m[3][column])
    return mat

def quick_inverse(m: ProjectionMatrix) -> ProjectionMatrix:
    '''Algorithm for inversing Rotation/Tranlation Matrices'''

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

    matrix.m[3][0] = -(m.m[3][0] * matrix.m[0][0] + m.m[3][1] *
                        matrix.m[1][0] + m.m[3][2] * matrix.m[2][0])
    matrix.m[3][1] = -(m.m[3][0] * matrix.m[0][1] + m.m[3][1] *
                        matrix.m[1][1] + m.m[3][2] * matrix.m[2][1])
    matrix.m[3][2] = -(m.m[3][0] * matrix.m[0][2] + m.m[3][1] *
                        matrix.m[1][2] + m.m[3][2] * matrix.m[2][2])
    matrix.m[3][3] = 1

    return matrix

