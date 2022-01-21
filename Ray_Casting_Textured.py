import os
import sys
import math
import time
import keyboard
import curses

from classes.Sprite_Class import Sprite
from functions.Command_Line_Font import command_line_font
from maps.Map_One import map_one
from maps.Map_Two import map_two
from maps.Map_Three import map_three
from maps.Map_Four import map_four
from maps.Map_Five import map_five
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
        self.player_a = 0.0             # Player Start Rotation

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
        self.update_map(map_one)

        self.map_height = len(self.map)
        self.map_width = len(self.map[0])

        # Initiat time variables
        self.tp1 = time.perf_counter()
        self.tp2 = time.perf_counter()
    
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


        if keyboard.is_pressed('1'):
            self.update_map(map_one)
        
        if keyboard.is_pressed('2'):
            self.update_map(map_two)

        if keyboard.is_pressed('3'):
            self.update_map(map_three)

        if keyboard.is_pressed('4'):
            self.update_map(map_four)

        if keyboard.is_pressed('5'):
            self.update_map(map_five)

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

        # Handle leftward movement & collision
        if keyboard.is_pressed('Q'):

            self.player_x -= math.sin(self.player_a + 1.5) * self.speed * elapsed_time
            self.player_y -= math.cos(self.player_a + 1.5) * self.speed * elapsed_time
            if self.map[int(self.player_y)][int(self.player_x)] == '#':

                self.player_x += math.sin(self.player_a + 1.5) * self.speed * elapsed_time
                self.player_y += math.cos(self.player_a + 1.5) * self.speed * elapsed_time

        # Handle rightward movement & collision
        if keyboard.is_pressed('E'):

            self.player_x -= math.sin(self.player_a - 1.5) * self.speed * elapsed_time
            self.player_y -= math.cos(self.player_a - 1.5) * self.speed * elapsed_time
            if self.map[int(self.player_y)][int(self.player_x)] == '#':

                self.player_x += math.sin(self.player_a - 1.5) * self.speed * elapsed_time
                self.player_y += math.cos(self.player_a - 1.5) * self.speed * elapsed_time


        for x in range(0, self.screen_width):

            # For each column, calculate the projected ray angle into world space
            ray_angle = (self.player_a - self.fov/2.0) + (float(x) / float(self.screen_width)) * self.fov

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

                        # Determine where on the wall the ray will hit. Break block boundry into 4 line segments
                        # When a wall is hit calculate the mid-point (0.5) since the wals are unit squares
                        block_mid_x =  test_x  + 0.5
                        block_mid_y = test_y + 0.5

                        test_point_x = self.player_x + eye_x * distance_to_wall
                        test_point_y = self.player_y + eye_y * distance_to_wall

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

                # Each Row
                if y < ceiling:
                    # Shading as black space
                    self.view.addstr(y, x, ' ')

                elif y > ceiling and y <= floor: # Drawing Wall

                    if distance_to_wall < self.depth:

                        sample_y = (y - ceiling) / (floor - ceiling)
                        glyph = self.wall.sample_glyph(sample_x, sample_y)
                        color = self.wall.sample_color(sample_x, sample_y)

                        self.screen[y][x] = glyph
                        self.screen[self.screen_height - 1][self.screen_width - 1] = ''
                        if color == 'R':
                            self.view.addstr(y, x, str(self.screen[y][x]), curses.color_pair(2))
                        else:
                            self.view.addstr(y, x, str(self.screen[y][x]), curses.color_pair(3))
                    
                    else:
                        self.view.addstr(y, x, ' ') # too far don't render


                else: # Floor

                    # Shading in as dark green pixle
                    if x == self.screen_width - 1 and y == self.screen_height -1:
                        self.view.addstr(y, x, '')
                    else:
                        self.view.addstr(y, x, ' ', curses.color_pair(1))

        # Refresh Screen
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
    print('Turn Left:   A')
    print('Turn Right:  D')
    print('')
    print('Move Left:   Q')
    print('Move Right:  E')
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
