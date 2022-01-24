class Sprite():
    ''' The Sprite class manipulates the imported sprite and is utilized for texture mapping
    
        Attributes:
            matrix (array): the color encoded 2d matrix of the sprite
            width (int): width of the 2d sprite matrix
            height (int): heigth of the 2d sprite matrix
            color_to_glyph_wall (dict): Converts color information in matrix_wall to glyph characters
    '''
    def __init__(self, matrix, color_to_glyph):
        ''' The constructor for Simulation class.
  
            Parameters:
                matrix (array): the color encoded 2d matrix of the sprite
                width (int): width of the 2d sprite matrix
                height (int): heigth of the 2d sprite matrix
                color_to_glyph_wall (dict): Converts color information in matrix_wall to glyph characters
        '''
        self.matrix = matrix
        self.width = len(matrix[0])
        self.height = len(matrix)
        self.color_to_glyph = color_to_glyph
    

    def sample_color(self, x, y):
        ''' For a given set of coordnates returns the glyph from the 2d sprite matrix
            
            Parameters:
                x (float): x coord where ray hit wall
                y (float): y coord where ray hit wall
        '''
        # Calculating the glyph index at given coordinates
        x = str(x).split('.')      
        x = '0.' + x[1]
        y = str(y).split('.')
        y = '0.' + y[1]
  
        sx = int(float(x) * self.width)
        sy = int(float(y) * self.height) - 1
      
        if sx < 0 or sx > self.width or sy < 0 or sy > self.height:
            return ' '

        return self.matrix[sy][sx]