'''Vector class for storing 2D vectors'''

from dataclasses import dataclass

@dataclass
class Vector:
    '''Holds 2D vector coordinates'''
    x: float = 0.0
    y: float = 0.0
    a: float = 0.0
