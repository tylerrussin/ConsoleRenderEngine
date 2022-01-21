import os
import sys
import math
import time
import json
import keyboard
import time
import curses
import numpy as np

from classes.Sprite_Class import Sprite
from functions.Command_Line_Font import command_line_font
from maps.Map_One import map_one
from maps.Map_Two import map_two
from maps.Map_Three import map_three
from maps.Map_Four import map_four
from maps.Map_Five import map_five
from maps.Map_Six import map_six
from sprites.Wall_Sprite import matrix_glyph
from sprites.Wall_Sprite import matrix_color

class Game():

    def __init__(self):
        self.screen_width = 320         # Console Screen Size X (columns)
        self.screen_height = 107        # Console Screen Size Y (rows)
        self.map_height = None
        self.map_width = None

        self.player_x = None
        self.player_y = None
        self.player_radians_list = [0.00, 1.57, 3.14, 4.71]        # Player angle
        self.player_radian_index = 0
        self.player_a = self.player_radians_list[self.player_radian_index]

        self.fov = 3.14159 / 4.0        # Field of View
        self.depth = 16.0               # Maximum rendering distance
        self.speed = 5.0                # Walking Speed

        self.screen = None
        self.tp1 = None
        self.tp2 = None
        self.map = None
        self.view = None
        self.wall = Sprite(matrix_glyph, matrix_color) # Initialize Sprite

    def on_user_create(self):

        # Create Screen Buffer
        self.screen = [[0 for x in range(self.screen_width)] for y in range(self.screen_height)]
        os.system(f"mode con: cols={self.screen_width} lines={self.screen_height}")
        os.system('color')

        # Inializing Curses
        self.view = curses.initscr()
        curses.curs_set(False)
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

        # Initiate with map_six
        self.update_map(map_six)

        self.map_height = len(self.map)
        self.map_width = len(self.map[0])

        # Initiat time variables
        self.tp1 = time.perf_counter()
        self.tp2 = time.perf_counter()

        # Checking if map file exists
        if os.path.exists('Hashed_Maps/test_map.json'):
            print('map file exists')
            # Opening JSON file
            f = open('Hashed_Maps/test_map.json')
            
            # returns JSON object as
            # a dictionary
            self.hashed_map = json.load(f)
            
            # Closing file
            f.close()
 
    
        else:
            # Have to create hashed map
            print('Creating hashed map. This may take a while...')
            self.create_hashed_map()
    
    def update_map(self, new_map):

        self.map = new_map
        # Setting Player start position and processing map
        for row, list in enumerate(self.map):
            for col, value in enumerate(list):
                if value == 'p':
                    self.player_x = float(col) + 0.5
                    self.player_y = float(row) + 0.5
                    self.map[row][col] = '.'

        self.player_a = 0.00

    def on_user_update(self):

        # We'll need time differential per frame to calculate modification
        # to movement speeds, to ensure consistant movement, as ray-tracing
        # is non-deterministic
        self.tp2 = time.perf_counter()
        elapsed_time = self.tp2 - self.tp1
        self.tp1 = self.tp2
        elapsed_time = elapsed_time

        # exits game loop
        if keyboard.is_pressed('P'):
            # Changing back to default font size

            curses.endwin()
            os.system(f"mode con: cols={120} lines={40}")
            command_line_font(16)
            sys.exit()


        # Handle CCW Rotation
        if keyboard.is_pressed('Q'):
            
            # Switching between views in negative direction
            if self.player_radian_index == 0:
                self.player_radian_index = 3
            else:
                self.player_radian_index =  self.player_radian_index - 1

            self.player_a = self.player_radians_list[self.player_radian_index]
            time.sleep(.25)

        # Handle CW Rotation
        if keyboard.is_pressed('E'):
            
            # Switching between views in positive direction
            if self.player_radian_index == 3:
                self.player_radian_index = 0
            else:
                self.player_radian_index =  self.player_radian_index + 1
            
            self.player_a = self.player_radians_list[self.player_radian_index]
            time.sleep(.25)

        # Handle Forwards movement & collision
        w_key = False
        if keyboard.is_pressed('W'):
            w_key = True
            self.player_x += math.sin(self.player_a) * self.speed * elapsed_time
            self.player_y += math.cos(self.player_a) * self.speed * elapsed_time
            if self.map[int(self.player_y)][int(self.player_x)] == '#':

                self.player_x -= math.sin(self.player_a) * self.speed * elapsed_time
                self.player_y -= math.cos(self.player_a) * self.speed * elapsed_time

        # Handle backwards movement & collision
        s_key = False
        if keyboard.is_pressed('S'):
            s_key = True
            self.player_x -= math.sin(self.player_a) * self.speed * elapsed_time
            self.player_y -= math.cos(self.player_a) * self.speed * elapsed_time
            if self.map[int(self.player_y)][int(self.player_x)] == '#':

                self.player_x += math.sin(self.player_a) * self.speed * elapsed_time
                self.player_y += math.cos(self.player_a) * self.speed * elapsed_time

        # Handle leftward movement & collision
        a_key = False
        if keyboard.is_pressed('A'):
            a_key = True
            self.player_x -= math.sin(self.player_a + 1.5) * self.speed * elapsed_time
            self.player_y -= math.cos(self.player_a + 1.5) * self.speed * elapsed_time
            if self.map[int(self.player_y)][int(self.player_x)] == '#':

                self.player_x += math.sin(self.player_a + 1.5) * self.speed * elapsed_time
                self.player_y += math.cos(self.player_a + 1.5) * self.speed * elapsed_time

        # Handle rightward movement & collision
        d_key = False
        if keyboard.is_pressed('D'):
            d_key = True
            self.player_x -= math.sin(self.player_a - 1.5) * self.speed * elapsed_time
            self.player_y -= math.cos(self.player_a - 1.5) * self.speed * elapsed_time
            if self.map[int(self.player_y)][int(self.player_x)] == '#':

                self.player_x += math.sin(self.player_a - 1.5) * self.speed * elapsed_time
                self.player_y += math.cos(self.player_a - 1.5) * self.speed * elapsed_time

        screen_string = self.hashed_map.get("({}, {}, {})".format(round(self.player_a, 2), round(self.player_y, 1), round(self.player_x, 1)))
        try:

            self.view.addstr(0, 0, screen_string)
            w_key = False
            s_key = False
            a_key = False
            d_key = False

        except:
            # moved into non existing coord. move back to previous posistion
            if w_key:
                self.player_x -= math.sin(self.player_a) * self.speed * elapsed_time
                self.player_y -= math.cos(self.player_a) * self.speed * elapsed_time
            if s_key:
                self.player_x += math.sin(self.player_a) * self.speed * elapsed_time
                self.player_y += math.cos(self.player_a) * self.speed * elapsed_time
            if a_key:
                self.player_x += math.sin(self.player_a + 1.5) * self.speed * elapsed_time
                self.player_y += math.cos(self.player_a + 1.5) * self.speed * elapsed_time
            if d_key:
                self.player_x += math.sin(self.player_a - 1.5) * self.speed * elapsed_time
                self.player_y += math.cos(self.player_a - 1.5) * self.speed * elapsed_time

            screen_string = self.hashed_map.get("({}, {}, {})".format(round(self.player_a, 2), round(self.player_y, 1), round(self.player_x, 1)))
            self.view.addstr(0, 0, screen_string)
        self.view.refresh()

        


    def create_hashed_map(self):
        hashed_map = {}

        # Traversing the entire map
        for radian_hash in self.player_radians_list:
            for y_hash in np.arange(0.0, self.map_height, 0.1):
                for x_hash in np.arange(0.0, self.map_width, 0.1):


                    # If we are in a wall
                    if self.map[int(y_hash)][int(x_hash)] == '#':
                        hashed_map.update({'({}, {}, {})'.format(round(radian_hash, 2), round(y_hash, 1), round(x_hash, 1)): '#'*(self.screen_width*self.screen_height)})
                    else:

                        for x in range(0, self.screen_width):

                            # For each column, calculate the projected ray angle into world space
                            ray_angle = (radian_hash - self.fov/2.0) + (float(x) / float(self.screen_width)) * self.fov

                            # Find distance to wall
                            step_size = 0.1         # Increment size for ray casting, decrease to increase
                            distance_to_wall = 0     #                                      resolution

                            hit_wall = False       # Set when ray hits wall block

                            eye_x = math.sin(ray_angle) # Unit vector for ray in player space
                            eye_y = math.cos(ray_angle)

                            sample_x = 0.0 # How far across the texture are we going to sample

                            # Incrementally cast ray from player, along ray angle, testing for 
                            # intersection with a block
                            while hit_wall == False and distance_to_wall < self.depth:

                                distance_to_wall += step_size
                                test_x = int(x_hash + eye_x * distance_to_wall)
                                test_y = int(y_hash + eye_y * distance_to_wall)

                                # Test if ray is out of bounds
                                if test_x < 0 or test_x >= self.map_width or test_y < 0 or test_y >= self.map_height:

                                    hit_wall = True         # Just set distance to maximum depth
                                    distance_to_wall = self.depth

                                else:

                                    # Ray is inbounds so test to see if the ray cell is a wall block
                                    if self.map[test_y][test_x] == '#':

                                        # Ray has hit wall
                                        hit_wall = True

                                        # Determine where on the wall the ray will hit. Break block boundry into 4 line segments
                                        # When a wall is hit calculate the mid-point (0.5) since the wals are unit squares
                                        block_mid_x =  test_x  + 0.5
                                        block_mid_y = test_y + 0.5

                                        test_point_x = x_hash + eye_x * distance_to_wall
                                        test_point_y = y_hash + eye_y * distance_to_wall

                                        test_angle = math.atan2((test_point_y - block_mid_y), (test_point_x - block_mid_x))

                                        if test_angle >= -3.14159 * 0.25 and test_angle < 3.14159 * 0.25:
                                            sample_x = test_point_y - test_y
                                        if test_angle >= 3.14159 * 0.25 and test_angle < 3.14159 * 0.75:
                                            sample_x = test_point_x - test_x
                                        if test_angle < -3.14159 * 0.25 and test_angle >= -3.14159 * 0.75:
                                            sample_x = test_point_x - test_x
                                        if test_angle >= 3.14159 * 0.75 or test_angle < -3.14159 * 0.75:
                                            sample_x = test_point_y - test_y



                            # Calculate distance to ceiling and floor
                            ceiling = float(self.screen_height/2.0) - self.screen_height / float(distance_to_wall)
                            floor = self.screen_height - ceiling

                            for y in range(0, self.screen_height):

                                self.screen[self.screen_height - 1][self.screen_width - 1] = ''
                                # Each Row
                                if y < ceiling:
                                    # Shading as black space
                                    self.screen[y][x] = ' '

                                elif y > ceiling and y <= floor: # Drawing Wall

                                    if distance_to_wall < self.depth:

                                        sample_y = (y - ceiling) / (floor - ceiling)
                                        color = self.wall.sample_color(sample_x, sample_y)

                                        self.screen[y][x] = color
                                            
                                    else:
                                        self.screen[y][x] = ' ' # too far don't render


                                else: # Floor

                                    # Shading in as dark green pixle
                                    self.screen[y][x] = 'G'


                        self.screen[self.screen_height - 1][self.screen_width - 1] = ''
                        screen_string =  ''.join(ele for sub in self.screen for ele in sub)
                        # Saving screen value in hash table
                        hashed_map.update({'({}, {}, {})'.format(round(radian_hash, 2), round(y_hash, 1), round(x_hash, 1)): screen_string})

        # Saving hashed map to class
        self.hashed_map = hashed_map

        # Saving the hashed map as json file for future use
        with open("Hashed_Maps/test_map.json", "w") as outfile:
            json.dump(hashed_map, outfile)

        
if __name__ == '__main__':

    # Initiate game loop
    game = Game()

    # Defining user controlls
    print('')
    print('Controls:')
    print('')
    print('Forward:     W')
    print('Backward:    S')
    print('')
    print('Turn Left:   Q')
    print('Turn Right:  E')
    print('')
    print('Move Left:   A')
    print('Move Right:  D')
    print('')
    print('Ouit:        P')
    print('')
    print('There are five maps to explore.')
    print('To change maps at any time press the following numbers.')
    print('')
    print('Map One:     1')
    print('Map Two:     2')
    print('Map Three:   3')
    print('Map Four:    4')
    print('Map Five:    5')
    print('')
    input('Press the Enter to continue...')

    # Command Line Formatting
    command_line_font(4)
    game.on_user_create()

    while True:
        game.on_user_update()

    # That's It!! - Tyler
