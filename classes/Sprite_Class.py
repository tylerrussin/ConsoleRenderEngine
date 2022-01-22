class Sprite():

    def __init__(self, matrix, color_to_glyph):
        self.matrix = matrix
        self.width = len(matrix[0])
        self.height = len(matrix)
        self.color_to_glyph = color_to_glyph
    
    def sample_color(self, x, y):
        x = str(x).split('.')
        x = '0.' + x[1]
        y = str(y).split('.')
        y = '0.' + y[1]
  
        sx = int(float(x) * self.width)
        sy = int(float(y) * self.height) - 1
      
        if sx < 0 or sx > self.width or sy < 0 or sy > self.height:
            return ' '

        return self.matrix[sy][sx]