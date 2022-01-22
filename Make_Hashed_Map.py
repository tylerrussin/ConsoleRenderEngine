from classes.Map_Hasher_Class import Map_Hasher
from maps.Map_One import map_one
from maps.Map_Two import map_two
from maps.Map_Three import map_three
from maps.Map_Four import map_four
from maps.Map_Five import map_five
from maps.Map_Six import map_six
from maps.Map_Seven import map_seven
from maps.Map_Eight import map_eight
from maps.Map_Nine import map_nine

if __name__ == '__main__':

    # Initiate Hash Class
    screen_width = 500
    screen_height = 200
    step_size = 0.01
    map_hashing = Map_Hasher(screen_width, screen_height, step_size)

    # Initiate with map
    map_hashing.update_map(map_nine, 'map_nine')

    print('You are about to begin map hashing')
    print(' ')
    input('Press the Enter to continue...')
    map_hashing.create_hashed_map()