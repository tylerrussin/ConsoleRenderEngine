'''Dataclasses holding mesh information'''

from typing import List
from dataclasses import dataclass, field


@dataclass
class Vector:
    '''Holds 3D vector coordinates'''

    x: int = 0
    y: int = 0
    z: int = 0
    w: int = 1

@dataclass
class Triangle:
    '''Holds 3 vectors that make up a triangle'''

    vec_1: Vector
    vec_2: Vector
    vec_3: Vector
    char: str = ' '

@dataclass
class ProjectionMatrix:
    '''Holds projected matrix values'''

    m: List[List[int]] = field(default_factory=lambda:
                               [[0 for x in range(4)] for y in range(4)])

@dataclass
class CubeMesh:
    '''Test unit cube'''

    tris: List[Triangle] = field(default_factory=lambda:
    [

        # South
        Triangle(Vector(0, 0, 0), Vector(0, 1, 0), Vector(1, 1, 0)),
        Triangle(Vector(0, 0, 0), Vector(1, 1, 0), Vector(1, 0, 0)),

        # East
        Triangle(Vector(1, 0, 0), Vector(1, 1, 0), Vector(1, 1, 1)),
        Triangle(Vector(1, 0, 0), Vector(1, 1, 1), Vector(1, 0, 1)),

        # North
        Triangle(Vector(1, 0, 1), Vector(1, 1, 1), Vector(0, 1, 1)),
        Triangle(Vector(1, 0, 1), Vector(0, 1, 1), Vector(0, 0, 1)),

        # West
        Triangle(Vector(0, 0, 1), Vector(0, 1, 1), Vector(0, 1, 0)),
        Triangle(Vector(0, 0, 1), Vector(0, 1, 0), Vector(0, 0, 0)),

        # Top
        Triangle(Vector(0, 1, 0), Vector(0, 1, 1), Vector(1, 1, 1)),
        Triangle(Vector(0, 1, 0), Vector(1, 1, 1), Vector(1, 1, 0)),

        # Bottom
        Triangle(Vector(1, 0, 1), Vector(0, 0, 1), Vector(0, 0, 0)),
        Triangle(Vector(1, 0, 1), Vector(0, 0, 0), Vector(1, 0, 0)),
    ])

@dataclass
class Mesh:
    '''Mesh loaded in from an obj file'''

    file_name: str
    tris: List[Triangle] = None

    def __post_init__(self):

        # Read in obj file
        file = open(self.file_name, "r", encoding="UTF-8")
        lines = file.readlines()
        file.close()

        triangles = []
        vectors = []

        for line in lines:

            # Create list of vectors
            if line[0] == 'v':
                line = line.split()
                vectors.append(Vector(float(line[1]), float(line[2]), float(line[3])))

            # Create list of triangles
            if line[0] == 'f':
                line = line.split()
                triangles.append(Triangle(vectors[int(line[1]) - 1],
                                          vectors[int(line[2]) - 1],
                                          vectors[int(line[3]) - 1]))

        self.tris = triangles
