import time

def key_press_e(player_a, player_y, player_x, player_radian_index, hashed_map, player_radians_list, speed, elapsed_time, map): 
    '''Handles the rightward rotation of the player through the E button'''
    # Handeling 4 point turn rotation     
    if hashed_map:
        if player_radian_index == 3:
            player_radian_index = 0
        else:
            player_radian_index =  player_radian_index + 1

        player_a = player_radians_list[player_radian_index]
        time.sleep(.25)
        
    # Handeling full circle rotation
    else:
        player_a += (speed * 0.75) * elapsed_time

    return player_a, player_y, player_x, player_radian_index


