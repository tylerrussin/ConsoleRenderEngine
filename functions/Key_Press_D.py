import math

def key_press_d(player_a, player_y, player_x, player_radian_index, hashed_map, player_radians_list, speed, elapsed_time, map): 
    '''Handles the rightward movement of the player through the D button'''
    # Handles changing player x, y coordinates
    try:                                                                    # With Hashing the player locations can be out of map, this is a safe gaurd   
        player_x -= math.sin(player_a - 1.57) * speed * elapsed_time
        player_y -= math.cos(player_a - 1.57) * speed * elapsed_time
        if map[int(player_y)][int(player_x)] == '#':

            player_x += math.sin(player_a - 1.57) * speed * elapsed_time
            player_y += math.cos(player_a - 1.57) * speed * elapsed_time

        return player_a, player_y, player_x, player_radian_index
        
    except:
        # Movement failed return the previous posisions
        return player_a, player_y, player_x, player_radian_index