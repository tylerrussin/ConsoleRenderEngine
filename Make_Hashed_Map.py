from classes.Map_Hasher_Class import Map_Hasher
from maps.Map_One import map_one
from maps.Map_Two import map_two


if __name__ == '__main__':

    # Initiate Hash Class
    map_hashing = Map_Hasher(screen_width = 500,
                             screen_height = 200, 
                             step_size = 0.01)

    # Initiate with map
    map_hashing.update_map(map_two, 'map_two')

    print('You are about to begin map hashing')
    print(' ')
    input('Press the Enter to continue...')
    map_hashing.create_hashed_map()

