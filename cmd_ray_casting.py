import os
import sys
import math
import time
import keyboard
import curses

from math import sqrt

screen_width = 120          # Console Screen Size X (columns)
screen_height = 40          # Console Screen Size Y (rows)
map_height = 16
map_width = 16

player_x = 14.7             # Player Start Position
player_y = 5.09
player_a = 0.0              # Player Start Rotation
fov = 3.14159 / 4.0        # Field of View
depth = 16.0               # Maximum rendering distance
speed = 5.0                # Walking Speed

# Create Screen Buffer
screen = [[0 for x in range(screen_width)] for y in range(screen_height)]
os.system(f"mode con: cols={screen_width} lines={screen_height}")

# Create Map of world space # = wall block, . = space
map = []
map.append(list('#########.......'))
map.append(list('#...............'))
map.append(list('#.......########'))
map.append(list('#..............#'))
map.append(list('#......##......#'))
map.append(list('#......##......#'))
map.append(list('#..............#'))
map.append(list('###............#'))
map.append(list('##.............#'))
map.append(list('#......####..###'))
map.append(list('#......#.......#'))
map.append(list('#......#.......#'))
map.append(list('#..............#'))
map.append(list('#......#########'))
map.append(list('#..............#'))
map.append(list('################'))

tp1 = time.perf_counter()
tp2 = time.perf_counter()

while 1:

    # We'll need time differential per frame to calculate modification
    # to movement speeds, to ensure consistant movement, as ray-tracing
    # is non-deterministic
    tp2 = time.perf_counter()
    elapsed_time = tp2 - tp1
    tp1 = tp2
    elapsed_time = elapsed_time

    # exits game loop
    if keyboard.is_pressed('q'):
        sys.exit()

    # Handle CCW Rotation
    if keyboard.is_pressed('A'):

        player_a -= (speed * 0.75) * elapsed_time

    # Handle CW Rotation
    if keyboard.is_pressed('D'):

        player_a += (speed * 0.75) * elapsed_time

    # Handle Forwards movement & collision
    if keyboard.is_pressed('W'):

        player_x += math.sin(player_a) * speed * elapsed_time
        player_y += math.cos(player_a) * speed * elapsed_time
        if map[int(player_y)][int(player_x)] == '#':

            player_x -= math.sin(player_a) * speed * elapsed_time
            player_y -= math.cos(player_a) * speed * elapsed_time

    # Handle backwards movement & collision
    if keyboard.is_pressed('S'):

        player_x -= math.sin(player_a) * speed * elapsed_time
        player_y -= math.cos(player_a) * speed * elapsed_time
        if map[int(player_y)][int(player_x)] == '#':

            player_x += math.sin(player_a) * speed * elapsed_time
            player_y += math.cos(player_a) * speed * elapsed_time

    for x in range(0, screen_width):

        # For each column, calculate the projected ray angle into world space
        ray_angle = (player_a - fov/2.0) + (float(x) / float(screen_width)) * fov

        # Find distance to wall
        step_size = 0.1         # Increment size for ray casting, decrease to increase
        distance_to_wall = 0     #                                      resolution

        hit_wall = False       # Set when ray hits wall block
        boundary = False      # Set when ray hits boundary between two wall blocks

        eye_x = math.sin(ray_angle) # Unit vector for ray in player space
        eye_y = math.cos(ray_angle)

        # Incrementally cast ray from player, along ray angle, testing for 
	    # intersection with a block
        while hit_wall == False and distance_to_wall < depth:

            distance_to_wall += step_size
            test_x = int(player_x + eye_x * distance_to_wall)
            test_y = int(player_y + eye_y * distance_to_wall)

            # Test if ray is out of bounds
            if test_x < 0 or test_x >= map_width or test_y < 0 or test_y >= map_height:

                hit_wall = True         # Just set distance to maximum depth
                distance_to_wall = depth

            else:

                # Ray is inbounds so test to see if the ray cell is a wall block
                if map[test_y][test_x] == '#':

                    # Ray has hit wall
                    hit_wall = True

                    # To highlight tile boundaries, cast a ray from each corner
                    # of the tile, to the player. The more coincident this ray
                    # is to the rendering ray, the closer we are to a tile 
                    # boundary, which we'll shade to add detail to the walls
                    p = []

                    # Test each corner of hit tile, storing the distance from
				    # the player, and the calculated dot product of the two rays
                    for tx in range(0,2):
                        for ty in range(0,2):

                            # Angle of corner to eye
                            vy = float(test_y) + ty - player_y
                            vx = float(test_x) + tx - player_x
                            d = sqrt(vx*vx + vy*vy)
                            dot = (eye_x * vx / d) + (eye_y * vy / d)
                            p.append((d, dot))
                    
                    # Sort Pairs from closest to farthest
                    p.sort(key=lambda x: x[0])

                    # First two/three are closest (we will never see all four)
                    bound = 0.01
                    if math.acos(p[0][1]) < bound: boundary = True
                    if math.acos(p[1][1]) < bound: boundary = True
                    if math.acos(p[2][1]) < bound: boundary = True




        # Calculate distance to ceiling and floor
        ceiling = float(screen_height/2.0) - screen_height / float(distance_to_wall)
        floor = screen_height - ceiling

        # Shader walls based on distance
        shade = ' '
        if distance_to_wall <= depth / 4.0:         shade = u'\u2588'     # Very Close
        elif distance_to_wall < depth / 3.0:        shade = u'\u2593'
        elif distance_to_wall < depth / 2.0:        shade = u'\u2592'
        elif distance_to_wall < depth:              shade = u'\u2591'
        else:                                       shade = ' '        # Too far away

        if boundary:       shade = ' ' # Black it out

        for y in range(0, screen_height):

            # Each Row
            if y < ceiling:
                screen[y][x] = ' '
            elif y > ceiling and y <= floor:
                screen[y][x] = shade
            else: # Floor

                # Shade floor based on distance
                b = 1.0 - ((float(y) - screen_height/2.0) / (float(screen_height) / 2.0))
                if b < 0.25:        shade_2 = '#'
                elif b < 0.5:       shade_2 = 'x'
                elif b < 0.75:      shade_2 = '.'
                elif b < 0.9:       shade_2 = '-'
                else:               shade_2 = " "
                screen[y][x] = shade_2



    # Display Stats
    view = curses.initscr()
    curses.curs_set(0)
    stats = f'X={"%.2f" % player_x}, Y={"%.2f" % player_y}, A={"%.2f" % player_a}, FPS={"%.2f" % (1.0 / elapsed_time)}'
    stats_window = curses.newwin(1, len(stats) + 1, 0, 0)
    stats_window.addstr(0, 0, stats)
    stats_window.refresh()

    # Display Map
    for nx in range(0, map_width):
        for ny in range(0, map_width):

            screen[ny + 1][nx] = map[ny][nx]
            
    screen[int(player_y)+1][int(player_x)] = 'P'

    # Display Frame (problem with the \0 in python 3.9. empty string also works. null termination only needed for c++ version)
    screen[screen_height - 1][screen_width - 1] = ''
    view.addstr(0, 0, ''.join(ele for sub in screen for ele in sub))
    view.refresh()
    

# That's It!! - Tyler
