import math

class Wall_sprite():

    def __init__(self):
        self.matrix_glyph = []
        self.matrix_color = []
        self.width = 32
        self.height = 32

    def make_matrix(self):

            # width will be 32 
            # Height will be 32
            matrix_glyph = []
            matrix_glyph.append(list('                                '))
            matrix_glyph.append(list('                                '))
            matrix_glyph.append(list('                                '))
            matrix_glyph.append(list('                                '))
            matrix_glyph.append(list('                                '))
            matrix_glyph.append(list('                                '))
            matrix_glyph.append(list('                                '))
            matrix_glyph.append(list('                                '))
            matrix_glyph.append(list('                                '))
            matrix_glyph.append(list('                                '))
            matrix_glyph.append(list('                                '))
            matrix_glyph.append(list('                                '))
            matrix_glyph.append(list('                                '))
            matrix_glyph.append(list('                                '))
            matrix_glyph.append(list('                                '))
            matrix_glyph.append(list('                                '))
            matrix_glyph.append(list('                                '))
            matrix_glyph.append(list('                                '))
            matrix_glyph.append(list('                                '))
            matrix_glyph.append(list('                                '))
            matrix_glyph.append(list('                                '))
            matrix_glyph.append(list('                                '))
            matrix_glyph.append(list('                                '))
            matrix_glyph.append(list('                                '))
            matrix_glyph.append(list('                                '))
            matrix_glyph.append(list('                                '))
            matrix_glyph.append(list('                                '))
            matrix_glyph.append(list('                                '))
            matrix_glyph.append(list('                                '))
            matrix_glyph.append(list('                                '))
            matrix_glyph.append(list('                                '))
            matrix_glyph.append(list('                                '))

            self.matrix_glyph = matrix_glyph

            matrix_color = []
            matrix_color.append(list('RRRWRRRRRRRWRRRRRRRWRRRRRRRWRRRR'))
            matrix_color.append(list('RRRWRRRRRRRWRRRRRRRWRRRRRRRWRRRR'))
            matrix_color.append(list('WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW'))
            matrix_color.append(list('RRRRRRRWRRRRRRRWRRRRRRRWRRRRRRRW'))
            matrix_color.append(list('RRRRRRRWRRRRRRRWRRRRRRRWRRRRRRRW'))
            matrix_color.append(list('WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW'))
            matrix_color.append(list('RRRWRRRRRRRWRRRRRRRWRRRRRRRWRRRR'))
            matrix_color.append(list('RRRWRRRRRRRWRRRRRRRWRRRRRRRWRRRR'))
            matrix_color.append(list('WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW'))
            matrix_color.append(list('RRRRRRRWRRRRRRRWRRRRRRRWRRRRRRRW'))
            matrix_color.append(list('RRRRRRRWRRRRRRRWRRRRRRRWRRRRRRRW'))
            matrix_color.append(list('WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW'))
            matrix_color.append(list('RRRWRRRRRRRWRRRRRRRWRRRRRRRWRRRR'))
            matrix_color.append(list('RRRWRRRRRRRWRRRRRRRWRRRRRRRWRRRR'))
            matrix_color.append(list('WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW'))
            matrix_color.append(list('RRRRRRRWRRRRRRRWRRRRRRRWRRRRRRRW'))
            matrix_color.append(list('RRRRRRRWRRRRRRRWRRRRRRRWRRRRRRRW'))
            matrix_color.append(list('WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW'))
            matrix_color.append(list('RRRWRRRRRRRWRRRRRRRWRRRRRRRWRRRR'))
            matrix_color.append(list('RRRWRRRRRRRWRRRRRRRWRRRRRRRWRRRR'))
            matrix_color.append(list('WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW'))
            matrix_color.append(list('RRRRRRRWRRRRRRRWRRRRRRRWRRRRRRRW'))
            matrix_color.append(list('RRRRRRRWRRRRRRRWRRRRRRRWRRRRRRRW'))
            matrix_color.append(list('WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW'))
            matrix_color.append(list('RRRWRRRRRRRWRRRRRRRWRRRRRRRWRRRR'))
            matrix_color.append(list('RRRWRRRRRRRWRRRRRRRWRRRRRRRWRRRR'))
            matrix_color.append(list('WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW'))
            matrix_color.append(list('RRRRRRRWRRRRRRRWRRRRRRRWRRRRRRRW'))
            matrix_color.append(list('RRRRRRRWRRRRRRRWRRRRRRRWRRRRRRRW'))
            matrix_color.append(list('WWWWWWWWWWWWWWWWWWWWWWWWWWWWWWWW'))
            matrix_color.append(list('RRRWRRRRRRRWRRRRRRRWRRRRRRRWRRRR'))
            matrix_color.append(list('RRRWRRRRRRRWRRRRRRRWRRRRRRRWRRRR'))

            self.matrix_color = matrix_color



    def sample_glyph(self, x, y):
        current_norm = 0
        x, _ = math.modf(x)
        y, _ = math.modf(y)
  
        sx = int(x * self.width)
        sy = int(y * self.height) - 1
      
        if sx < 0 or sx > self.width or sy < 0 or sy > self.height:
            return '#'
        # if x > 0 and x < 1:
        #     for x_index in range(32):
        #         if x >= current_norm and x < current_norm + 0.03125:
        #             # all we needed was x_index
        #             break

        #         current_norm = current_norm + 0.03125
        #     x_coord = x_index
            
        #     current_norm = 0
        #     for y_index in range(32):
        #         if y >= current_norm and y < current_norm + 0.03125:
        #             # all we needed was x_index
        #             break
                    
        #         current_norm = current_norm + 0.03125
        #     y_coord = y_index
        # else:
        #     return '$'


        return self.matrix_glyph[sy][sx]

    def sample_color(self, x, y):
        current_norm = 0
        x, _ = math.modf(x)
        y, _ = math.modf(y)
  
        sx = int(x * self.width)
        sy = int(y * self.height) - 1
      
        if sx < 0 or sx > self.width or sy < 0 or sy > self.height:
            return '#'

        # if x > 0 and x < 1:
        #     for x_index in range(32):
        #         if x >= current_norm and x < current_norm + 0.03125:
        #             # all we needed was x_index
        #             break

        #         current_norm = current_norm + 0.03125
        #     x_coord = x_index
            
        #     current_norm = 0
        #     for y_index in range(32):
        #         if y >= current_norm and y < current_norm + 0.03125:
        #             # all we needed was x_index
        #             break
                    
        #         current_norm = current_norm + 0.03125
        #     y_coord = y_index
        # else:
        #     return '$'


        return self.matrix_color[sy][sx]