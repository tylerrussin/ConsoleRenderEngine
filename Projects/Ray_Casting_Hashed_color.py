from classes.Simulation_Class import Simulation
from sprites import Wall_Sprite
from maps.Map_One import map_one
from maps.Map_Two import map_two


if __name__ == '__main__':

    # Initiate simulation loop
    # Hashed Colored Simulation
    game = Simulation(screen_width = 500, 
                    screen_height = 200,
                    console_font_size= 2, 
                    simulation_type = 'hashed', 
                    step_size = 0.01, 
                    matrix_wall = Wall_Sprite.matrix, 
                    color_to_glyph_wall = Wall_Sprite.color_to_glyph,
                    greyscale = False)

    # Defining user controlls
    print('')
    print('Controls:')
    print('')
    print('Forward:     W')
    print('Backward:    S')
    print('Move Left:   A')
    print('Move Right:  D')
    print('')
    print('Turn Left:   Q')
    print('Turn Right:  E')
    print('')
    print('Ouit:        P')
    print('')
    print('')
    input('Press the Enter to continue...')

    # Initiate with map_six
    game.update_map(map_two, 'map_two')
    game.on_user_create()

    while True:
        game.on_user_update()

