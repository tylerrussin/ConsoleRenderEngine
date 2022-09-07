'''Dataclasses holding mesh information'''

from typing import List
from dataclasses import dataclass, field


@dataclass
class Vector:
    '''Holds 3D vector coordinates'''

    x: int = 0
    y: int = 0
    z: int = 0

@dataclass
class Triangle:
    '''Holds 3 vectors that make up a triangle'''

    vec_1: int
    vec_2: int
    vec_3: int
    char: str = ' '

@dataclass
class ProjectionMatrix:
    '''Holds projected matrix values'''

    matrix: List[List[int]] = field(default_factory=lambda:
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
        f = open(self.file, "r")
        lines = f.readlines()
        f.close()

        triangles = []
        verts = []

        for line in lines:

            # Create list of vectors
            if line[0] == 'v':
                line = line.split()
                verts.append(Vector(float(line[1]), float(line[2]), float(line[3])))

            # Create list of triangles
            if line[0] == 'f':
                line = line.split()
                triangles.append(Triangle(verts[int(line[1]) - 1],
                                          verts[int(line[2]) - 1],
                                          verts[int(line[3]) - 1]))

        self.tris = triangles
