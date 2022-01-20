import math

class Sprite():

    def __init__(self, matrix_glyph, matrix_color):
        self.matrix_glyph = matrix_glyph
        self.matrix_color = matrix_color
        self.width = len(matrix_glyph[0])
        self.height = len(matrix_glyph)
    
    def sample_glyph(self, x, y):
        x, _ = math.modf(x)
        y, _ = math.modf(y)
  
        sx = int(x * self.width)
        sy = int(y * self.height) - 1
      
        if sx < 0 or sx > self.width or sy < 0 or sy > self.height:
            return ' '

        return self.matrix_glyph[sy][sx]

    def sample_color(self, x, y):
        x, _ = math.modf(x)
        y, _ = math.modf(y)
  
        sx = int(x * self.width)
        sy = int(y * self.height) - 1
      
        if sx < 0 or sx > self.width or sy < 0 or sy > self.height:
            return ' '

        return self.matrix_color[sy][sx]