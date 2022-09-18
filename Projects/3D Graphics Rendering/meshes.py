'''Classes for importing and creating meshes'''
from dataclasses import dataclass, field

import vectors


@dataclass
class Triangle:
    '''Holds 3 vectors that make up a triangle'''

    vec_1: vectors.Vector
    vec_2: vectors.Vector
    vec_3: vectors.Vector
    sym: str = ''
    col: str = ''


@dataclass
class CubeMesh:
    '''Test unit cube'''

    tris: list[Triangle] = field(default_factory=lambda:
    [

        # South
        Triangle(vectors.Vector(0, 0, 0), vectors.Vector(0, 1, 0), vectors.Vector(1, 1, 0)),
        Triangle(vectors.Vector(0, 0, 0), vectors.Vector(1, 1, 0), vectors.Vector(1, 0, 0)),

        # East
        Triangle(vectors.Vector(1, 0, 0), vectors.Vector(1, 1, 0), vectors.Vector(1, 1, 1)),
        Triangle(vectors.Vector(1, 0, 0), vectors.Vector(1, 1, 1), vectors.Vector(1, 0, 1)),

        # North
        Triangle(vectors.Vector(1, 0, 1), vectors.Vector(1, 1, 1), vectors.Vector(0, 1, 1)),
        Triangle(vectors.Vector(1, 0, 1), vectors.Vector(0, 1, 1), vectors.Vector(0, 0, 1)),

        # West
        Triangle(vectors.Vector(0, 0, 1), vectors.Vector(0, 1, 1), vectors.Vector(0, 1, 0)),
        Triangle(vectors.Vector(0, 0, 1), vectors.Vector(0, 1, 0), vectors.Vector(0, 0, 0)),

        # Top
        Triangle(vectors.Vector(0, 1, 0), vectors.Vector(0, 1, 1), vectors.Vector(1, 1, 1)),
        Triangle(vectors.Vector(0, 1, 0), vectors.Vector(1, 1, 1), vectors.Vector(1, 1, 0)),

        # Bottom
        Triangle(vectors.Vector(1, 0, 1), vectors.Vector(0, 0, 1), vectors.Vector(0, 0, 0)),
        Triangle(vectors.Vector(1, 0, 1), vectors.Vector(0, 0, 0), vectors.Vector(1, 0, 0)),
    ])


@dataclass
class LoadMesh:
    '''Mesh loaded in from an obj file'''

    file_name: str
    tris: list[Triangle] = None

    def __post_init__(self):

        # Read in obj file
        file = open(self.file_name, "r", encoding="UTF-8")
        lines = file.readlines()
        file.close()

        triangles_list = []
        vectors_list = []

        for line in lines:

            # Create list of vectors_list
            if line[0] == 'v':
                line = line.split()
                vectors_list.append(vectors.Vector(float(line[1]), float(line[2]), float(line[3])))

            # Create list of triangles_list
            if line[0] == 'f':
                line = line.split()
                triangles_list.append(Triangle(vectors_list[int(line[1]) - 1],
                                          vectors_list[int(line[2]) - 1],
                                          vectors_list[int(line[3]) - 1]))

        self.tris = triangles_list
