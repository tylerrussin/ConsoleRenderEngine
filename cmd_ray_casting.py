import os
import sys
import math
import time
import keyboard
import curses

from maps.Map_One import map_one
from maps.Map_Two import map_two
from maps.Map_Three import map_three
from maps.Map_Four import map_four
from maps.Map_Five import map_five
from functions.Map_Select import map_select

class Game():

    # Have player select map level
    map_dict = {'Map One': map_one,
                'Map Two': map_two,
                'Map Three': map_three,
                'Map Four': map_four,
                'Map Five': map_five}


    def __init__(self):
        self.screen_width = 120         # Console Screen Size X (columns)
        self.screen_height = 40         # Console Screen Size Y (rows)

        self.map_height = 16
        self.map_width = 16

        self.player_x = None
        self.player_y = None
        self.player_a = 0.0             # Player Start Rotation

        self.fov = 3.14159 / 4.0        # Field of View
        self.depth = 16.0               # Maximum rendering distance
        self.speed = 5.0                # Walking Speed

        self.screen = None

        self.tp1 = None
        self.tp2 = None

        self.map = None

    def on_user_create(self):
        # Create Screen Buffer
        self.screen = [[0 for x in range(self.screen_width)] for y in range(self.screen_height)]
        os.system(f"mode con: cols={self.screen_width} lines={self.screen_height}")

        self.map = map_select(self.map_dict)

        # Setting Player start position and processing map
        for row, list in enumerate(self.map):
            for col, value in enumerate(list):
                if value == 'p':
                    self.player_x = float(col) + 0.5
                    self.player_y = float(row) + 0.5
                    self.map[row][col] = '.'

        # Initiat time variables
        self.tp1 = time.perf_counter()
        self.tp2 = time.perf_counter()

    def on_user_update(self):
         # We'll need time differential per frame to calculate modification
        # to movement speeds, to ensure consistant movement, as ray-tracing
        # is non-deterministic
        self.tp2 = time.perf_counter()
        elapsed_time = self.tp2 - self.tp1
        self.tp1 = self.tp2
        elapsed_time = elapsed_time

        # exits game loop
        if keyboard.is_pressed('Q'):
            sys.exit()

        # Handle CCW Rotation
        if keyboard.is_pressed('A'):

            self.player_a -= (self.speed * 0.75) * elapsed_time

        # Handle CW Rotation
        if keyboard.is_pressed('D'):

            self.player_a += (self.speed * 0.75) * elapsed_time

        # Handle Forwards movement & collision
        if keyboard.is_pressed('W'):

            self.player_x += math.sin(self.player_a) * self.speed * elapsed_time
            self.player_y += math.cos(self.player_a) * self.speed * elapsed_time
            if self.map[int(self.player_y)][int(self.player_x)] == '#':

                self.player_x -= math.sin(self.player_a) * self.speed * elapsed_time
                self.player_y -= math.cos(self.player_a) * self.speed * elapsed_time

        # Handle backwards movement & collision
        if keyboard.is_pressed('S'):

            self.player_x -= math.sin(self.player_a) * self.speed * elapsed_time
            self.player_y -= math.cos(self.player_a) * self.speed * elapsed_time
            if self.map[int(self.player_y)][int(self.player_x)] == '#':

                self.player_x += math.sin(self.player_a) * self.speed * elapsed_time
                self.player_y += math.cos(self.player_a) * self.speed * elapsed_time

        for x in range(0, self.screen_width):

            # For each column, calculate the projected ray angle into world space
            ray_angle = (self.player_a - self.fov/2.0) + (float(x) / float(self.screen_width)) * self.fov

            # Find distance to wall
            step_size = 0.1         # Increment size for ray casting, decrease to increase
            distance_to_wall = 0     #                                      resolution

            hit_wall = False       # Set when ray hits wall block
            boundary = False      # Set when ray hits boundary between two wall blocks

            eye_x = math.sin(ray_angle) # Unit vector for ray in player space
            eye_y = math.cos(ray_angle)

            # Incrementally cast ray from player, along ray angle, testing for 
            # intersection with a block
            while hit_wall == False and distance_to_wall < self.depth:

                distance_to_wall += step_size
                test_x = int(self.player_x + eye_x * distance_to_wall)
                test_y = int(self.player_y + eye_y * distance_to_wall)

                # Test if ray is out of bounds
                if test_x < 0 or test_x >= self.map_width or test_y < 0 or test_y >= self.map_height:

                    hit_wall = True         # Just set distance to maximum depth
                    distance_to_wall = self.depth

                else:

                    # Ray is inbounds so test to see if the ray cell is a wall block
                    if self.map[test_y][test_x] == '#':

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
                                vy = float(test_y) + ty - self.player_y
                                vx = float(test_x) + tx - self.player_x
                                d = math.sqrt(vx*vx + vy*vy)
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
            ceiling = float(self.screen_height/2.0) - self.screen_height / float(distance_to_wall)
            floor = self.screen_height - ceiling

            # Shader walls based on distance
            shade = ' '
            if distance_to_wall <= self.depth / 4.0:         shade = u'\u2588'     # Very Close
            elif distance_to_wall < self.depth / 3.0:        shade = u'\u2593'
            elif distance_to_wall < self.depth / 2.0:        shade = u'\u2592'
            elif distance_to_wall < self.depth:              shade = u'\u2591'
            else:                                       shade = ' '        # Too far away

            if boundary:       shade = ' ' # Black it out

            for y in range(0, self.screen_height):

                # Each Row
                if y < ceiling:
                    self.screen[y][x] = ' '
                elif y > ceiling and y <= floor:
                    self.screen[y][x] = shade
                else: # Floor

                    # Shade floor based on distance
                    b = 1.0 - ((float(y) - self.screen_height/2.0) / (float(self.screen_height) / 2.0))
                    if b < 0.25:        shade_2 = '#'
                    elif b < 0.5:       shade_2 = 'x'
                    elif b < 0.75:      shade_2 = '.'
                    elif b < 0.9:       shade_2 = '-'
                    else:               shade_2 = " "
                    self.screen[y][x] = shade_2



        # Display Stats
        view = curses.initscr()
        curses.curs_set(0)
        stats = f'X={"%.2f" % self.player_x}, Y={"%.2f" % self.player_y}, A={"%.2f" % self.player_a}, FPS={"%.2f" % (1.0 / elapsed_time)}'
        stats_window = curses.newwin(1, len(stats) + 1, 0, 0)
        stats_window.addstr(0, 0, stats)
        stats_window.refresh()

        # Display Map
        for nx in range(0, self.map_width):
            for ny in range(0, self.map_width):

                self.screen[ny + 1][nx] = self.map[ny][nx]
                
        self.screen[int(self.player_y)+1][int(self.player_x)] = 'p'

        # Display Frame (problem with the \0 in python 3.9. empty string also works. null termination only needed for c++ version)
        self.screen[self.screen_height - 1][self.screen_width - 1] = ''
        view.addstr(0, 0, ''.join(ele for sub in self.screen for ele in sub))
        view.refresh()
        

# Initiate game loop
game = Game()
game.on_user_create()
while True:
    game.on_user_update()    


# That's It!! - Tyler
