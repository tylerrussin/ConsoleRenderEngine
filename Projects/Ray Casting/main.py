'''Ray Casting in the command line'''

import sys
import math
import time

import keyboard

import vectors
from data import game_map, wall_sprite

# Path to console_render_engine.py
sys.path.append('../..')

import console_render_engine


if __name__ == '__main__':

    CMD_FONT = 5                      # Console ASCII font size
    SCREEN_WIDTH = 256                # Console Screen Size X (columns)
    SCREEN_HEIGHT = 127               # Console Screen Size Y (rows)

    # Initialize console
    cmd_engine = console_render_engine.ConsoleRenderEngine(CMD_FONT, SCREEN_WIDTH, SCREEN_HEIGHT)
    cmd_engine.on_user_create()

    game_map = game_map.matrix
    wall_sprite = wall_sprite.matrix

    # Game map dimenstions
    map_width = len(game_map[0])
    map_height = len(game_map)

    # Player vector
    v_player = vectors.Vector(14.7, 5.09, 0.0)

    field_of_view = 3.14159 / 4.0
    max_depth = 16.0
    player_speed = 5.0

    tp1 = time.perf_counter()
    tp2 = time.perf_counter()


    # Game loop
    while 1:

        cmd_engine.reset_screen()

        # Calculate time differential
        tp2 = time.perf_counter()
        elapsed_time = tp2 - tp1
        tp1 = tp2


        # Quit simulation
        if keyboard.is_pressed('P'):
            cmd_engine.on_user_destroy()
            sys.exit()

        # Handle Left Rotation
        if keyboard.is_pressed('Q'):
            v_player.a -= (player_speed * 0.75) * elapsed_time

        # Handle Right Rotation
        if keyboard.is_pressed('E'):
            v_player.a += (player_speed * 0.75) * elapsed_time

        # Handle Left & collision
        if keyboard.is_pressed('A'):

            v_player.x -= math.sin(v_player.a + 1.5) * player_speed * elapsed_time
            v_player.y -= math.cos(v_player.a + 1.5) * player_speed * elapsed_time
            if game_map[int(v_player.y)][int(v_player.x)] == '#':

                v_player.x += math.sin(v_player.a + 1.5) * player_speed * elapsed_time
                v_player.y += math.cos(v_player.a + 1.5) * player_speed * elapsed_time

        # Handle Right movement & collision
        if keyboard.is_pressed('D'):

            v_player.x -= math.sin(v_player.a - 1.5) * player_speed * elapsed_time
            v_player.y -= math.cos(v_player.a - 1.5) * player_speed * elapsed_time
            if game_map[int(v_player.y)][int(v_player.x)] == '#':

                v_player.x += math.sin(v_player.a - 1.5) * player_speed * elapsed_time
                v_player.y += math.cos(v_player.a - 1.5) * player_speed * elapsed_time

        # Handle Forwards movement & collision
        if keyboard.is_pressed('W'):

            v_player.x += math.sin(v_player.a) * player_speed * elapsed_time
            v_player.y += math.cos(v_player.a) * player_speed * elapsed_time
            if game_map[int(v_player.y)][int(v_player.x)] == '#':

                v_player.x -= math.sin(v_player.a) * player_speed * elapsed_time
                v_player.y -= math.cos(v_player.a) * player_speed * elapsed_time

        # Handle backwards movement & collision
        if keyboard.is_pressed('S'):

            v_player.x -= math.sin(v_player.a) * player_speed * elapsed_time
            v_player.y -= math.cos(v_player.a) * player_speed * elapsed_time
            if game_map[int(v_player.y)][int(v_player.x)] == '#':

                v_player.x += math.sin(v_player.a) * player_speed * elapsed_time
                v_player.y += math.cos(v_player.a) * player_speed * elapsed_time

        # Origin vector for digital differential analysis
        ray_start = vectors.Vector(v_player.x, v_player.y)


        for x in range(0, SCREEN_WIDTH):

            # For each column, calculate the projected ray angle into world space
            ray_angle = (v_player.a - field_of_view/2.0) + (x / SCREEN_WIDTH) * field_of_view

             # Unit vector for ray in player space
            ray_dir = vectors.Vector(math.sin(ray_angle), math.cos(ray_angle))

            if ray_dir.x == 0:
                ray_dir.x += 0.001
            if ray_dir.y == 0:
                ray_dir.y += 0.001

            ray_unit_step_size = vectors.Vector(abs(1 / ray_dir.x), abs(1 / ray_dir.y))

            map_check = vectors.Vector(int(ray_start.x), int(ray_start.y))
            ray_length_1d = vectors.Vector()
            step = vectors.Vector()

            # Establish staring conditons
            if ray_dir.x < 0:
                step.x = -1
                ray_length_1d.x = (ray_start.x - map_check.x) * ray_unit_step_size.x
            else:
                step.x = 1
                ray_length_1d.x = (map_check.x + 1 - ray_start.x) * ray_unit_step_size.x

            if ray_dir.y < 0:
                step.y = -1
                ray_length_1d.y = (ray_start.y - map_check.y) * ray_unit_step_size.y
            else:
                step.y = 1
                ray_length_1d.y = (map_check.y + 1 - ray_start.y) * ray_unit_step_size.y

            # Perform "walk" until colision or range check
            hit_wall = False
            max_depth = 16
            distance_to_wall = 0

            while not hit_wall and distance_to_wall < max_depth:

                # Walk along shortest path
                if ray_length_1d.x < ray_length_1d.y:
                    map_check.x += step.x
                    distance_to_wall = ray_length_1d.x
                    ray_length_1d.x += ray_unit_step_size.x

                else:
                    map_check.y += step.y
                    distance_to_wall = ray_length_1d.y
                    ray_length_1d.y += ray_unit_step_size.y

                # Test tile at new test point
                if (map_check.x >= 0 and map_check.x < map_width and
                    map_check.y >= 0 and map_check.y < map_height):

                    if game_map[map_check.y][map_check.x] == '#':

                        hit_wall = True


            # Calculate intersection location
            if hit_wall:
                intersection = vectors.Vector(ray_start.x + ray_dir.x * distance_to_wall,
                                              ray_start.y + ray_dir.y * distance_to_wall)

            sample_x = 0

            # Determine where on the wall the ray will hit. Break block boundry into 4 line segments
            # When a wall is hit calculate the mid-point (0.5) since the walls are unit squares
            block_mid_x =  map_check.x  + 0.5
            block_mid_y = map_check.y + 0.5

            test_angle = math.atan2((intersection.y - block_mid_y), (intersection.x - block_mid_x))

            if test_angle >= -3.14159 * 0.25 and test_angle < 3.14159 * 0.25:
                sample_x = intersection.y - map_check.y
            elif test_angle >= 3.14159 * 0.25 and test_angle < 3.14159 * 0.75:
                sample_x = intersection.x - map_check.x
            elif test_angle < -3.14159 * 0.25 and test_angle >= -3.14159 * 0.75:
                sample_x = intersection.x - map_check.x
            elif test_angle >= 3.14159 * 0.75 or test_angle < -3.14159 * 0.75:
                sample_x = intersection.y - map_check.y


            # Calculate distance to ceiling and floor
            ceiling = float(SCREEN_HEIGHT/2.0) - SCREEN_HEIGHT / float(distance_to_wall)
            floor = SCREEN_HEIGHT - ceiling


            for y in range(0, SCREEN_HEIGHT):

                # Render ceiling
                if y < ceiling:
                    cmd_engine.draw(x, y, ' ', [cmd_engine.FG_BLACK, cmd_engine.BG_BLACK])

                # Render wall
                elif y > ceiling and y <= floor:

                    if distance_to_wall < max_depth:
                        sample_y = (y - ceiling) / (floor - ceiling)

                        # Sample texture
                        sample_x = str(sample_x).split('.')      
                        sample_x = '0.' + sample_x[1]
                        sample_y = str(sample_y).split('.')
                        sample_y = '0.' + sample_y[1]

                        sx = int(float(sample_x) * len(wall_sprite[0]))
                        sy = int(float(sample_y) * len(wall_sprite)) - 1

                        color = wall_sprite[sy][sx]

                        if color == 'R':
                            cmd_engine.draw(x, y, ' ', [cmd_engine.FG_BLACK,
                                                        cmd_engine.BG_DARK_RED])
                        else:
                            cmd_engine.draw(x, y, ' ', [cmd_engine.FG_BLACK, cmd_engine.BG_WHITE])

                    else:
                        cmd_engine.draw(x, y, ' ', [cmd_engine.FG_BLACK, cmd_engine.BG_BLACK])

                # Render floow
                else:
                    cmd_engine.draw(x, y, ' ', [cmd_engine.FG_BLACK, cmd_engine.BG_DARK_GREEN])


        # Display Stats
        cmd_engine.reset_title(f'X={round(v_player.x, 2)}, Y={round(v_player.y, 2)}, A={round(v_player.a, 2)}, FPS={round(1.0 / elapsed_time, 2)}')

        cmd_engine.draw(SCREEN_WIDTH - 1, SCREEN_HEIGHT - 1, '\0', [cmd_engine.FG_WHITE,
                                                                    cmd_engine.BG_BLACK])
        cmd_engine.display_screen()
