from classes.Simulation_Class import Simulation
from sprites import Wall_Sprite
from maps.Map_One import map_one
from maps.Map_Two import map_two
from maps.Map_Three import map_three
from maps.Map_Four import map_four
from maps.Map_Five import map_five
from maps.Map_Six import map_six
from maps.Map_Seven import map_seven
from maps.Map_Eight import map_eight


if __name__ == '__main__':

    # Initiate simpulation loop

    # Classic
    game = Simulation(screen_width = 120, 
                      screen_height = 40,
                      console_font_size= 16, 
                      simulation_type = 'classic', 
                      step_size = 0.1, 
                      matrix_wall = Wall_Sprite.matrix, 
                      color_to_glyph_wall = Wall_Sprite.color_to_glyph)

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
    game.update_map(map_seven, 'map_seven')
    game.on_user_create()

    while True:
        game.on_user_update()

    # That's It!! - Tyler



    # Potenially put in target objects into the hashed dictionary. the only problem is they can't be deleted if you do this. however any point traking can be disabled.
# for the fire ball it can be a simle animation that just view.add() over the hased screen and just goes smaller for a number of steps dependent on target coords vs player coords.


# Given the fact that I have to move on to other projects i am proposing ot
# - leave target and fireball rendering for another time
# - leave imporved ray casting for another time as well
# - Using memory adding and deleting for large scale world
# - Using the half block ascii character you could render two lines in one pixel (less memory space but more view.ads() calling)


# Things to finish
# - the read me
# - the make breaking when using hased map (out of bounds error)
# - Implement the improved color rendering concepts discusted
# - Amazon s3 bucket large hashed map connection
# - Create executable file versions for the main simulations (one for the large hashed map and one for classic mode)
# - Final documentaion and code cleaning