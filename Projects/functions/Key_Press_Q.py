import time

def key_press_q(player_a, player_y, player_x, player_radian_index, simulation_type, player_radians_list, speed, elapsed_time, map):
    '''Handles the leftward rotation of the player through the Q button''' 
    # Handeling 4 point turn rotation     
    if simulation_type == 'hashed':
        if player_radian_index == 0:
            player_radian_index = 3
        else:
            player_radian_index =  player_radian_index - 1

        player_a = player_radians_list[player_radian_index]
        time.sleep(.25)
        
    # Handeling full circle rotation
    else:
        player_a -= (speed * 0.75) * elapsed_time

    return player_a, player_y, player_x, player_radian_index