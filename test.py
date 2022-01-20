from sprites.Wall_Sprite import Wall_sprite

wall = Wall_sprite()

wall.make_matrix()

print(wall.sample_glyph(.5, .5))