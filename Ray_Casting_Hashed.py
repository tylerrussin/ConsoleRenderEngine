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
from maps.Map_Seven import map_seven
from maps.Map_Eight import map_eight
from sprites.Wall_Sprite import matrix_glyph
from sprites.Wall_Sprite import matrix_color
from sprites.Wall_Sprite import color_to_glyph

class Game():

    shade_dict = {' ': 4,  # it is C for map eight!!!
                  'W': 3,
                  'R': 2,
                  'G': 1}

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
        self.wall = Sprite(matrix_glyph, matrix_color, color_to_glyph) # Initialize Sprite

        self.screen_string = None

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
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLACK)

        # Initiate with map
        self.update_map(map_seven)

        self.map_height = len(self.map)
        self.map_width = len(self.map[0])

        # Initiat time variables
        self.tp1 = time.perf_counter()
        self.tp2 = time.perf_counter()

        # Checking if map file exists
        if os.path.exists('classes/Hashed_Maps/map_seven.json'):
            print('map file exists')
            # Opening JSON file
            f = open('classes/Hashed_Maps/map_seven.json')
            
            # returns JSON object as
            # a dictionary
            self.hashed_map = json.load(f)
            
            # Closing file
            f.close()
 
    
        else:
            # Have to create hashed map
            print('The hashed map specified does not exist...')
            
    
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
            del self.hashed_map
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
            self.player_x -= math.sin(self.player_a + 1.57) * self.speed * elapsed_time
            self.player_y -= math.cos(self.player_a + 1.57) * self.speed * elapsed_time
            if self.map[int(self.player_y)][int(self.player_x)] == '#':

                self.player_x += math.sin(self.player_a + 1.57) * self.speed * elapsed_time
                self.player_y += math.cos(self.player_a + 1.57) * self.speed * elapsed_time

        # Handle rightward movement & collision
        d_key = False
        if keyboard.is_pressed('D'):
            d_key = True
            self.player_x -= math.sin(self.player_a - 1.57) * self.speed * elapsed_time
            self.player_y -= math.cos(self.player_a - 1.57) * self.speed * elapsed_time
            if self.map[int(self.player_y)][int(self.player_x)] == '#':

                self.player_x += math.sin(self.player_a - 1.57) * self.speed * elapsed_time
                self.player_y += math.cos(self.player_a - 1.57) * self.speed * elapsed_time

        # Get current screen
        self.screen_string = self.hashed_map.get("({}, {}, {})".format(round(self.player_a, 2), round(self.player_y, 1), round(self.player_x, 1)))
        try:

            self.render_screen()
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
                self.player_x += math.sin(self.player_a + 1.57) * self.speed * elapsed_time
                self.player_y += math.cos(self.player_a + 1.57) * self.speed * elapsed_time
            if d_key:
                self.player_x += math.sin(self.player_a - 1.57) * self.speed * elapsed_time
                self.player_y += math.cos(self.player_a - 1.57) * self.speed * elapsed_time

            self.screen_string = self.hashed_map.get("({}, {}, {})".format(round(self.player_a, 2), round(self.player_y, 1), round(self.player_x, 1)))
            self.render_screen()
            
        
    def render_screen(self):
        screen_list = [char for char in self.screen_string]
        index = 0
        for char in screen_list:
            coord_str = str(index / self.screen_width)
            coord_str = coord_str.split('.')
            y, x = coord_str[0], '0.' + coord_str[1]
            index = index + 1
            y = int(y)
            x = int(float(x) * self.screen_width)
            self.view.addstr(y, x, ' ', curses.color_pair(self.shade_dict[char]))

        self.view.refresh()

        
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