import os
import sys

script_dir = os.path.dirname( __file__ )
main_dir = os.path.join( script_dir, '..' )
sys.path.append( main_dir )

import math
import time
import keyboard
import curses
import json

from classes.Sprite_Class import Sprite
from functions.Command_Line_Font import command_line_font

from functions.Key_Press_A import key_press_a
from functions.Key_Press_D import key_press_d
from functions.Key_Press_W import key_press_w
from functions.Key_Press_S import key_press_s
from functions.Key_Press_Q import key_press_q
from functions.Key_Press_E import key_press_e
from maps.Map_One import map_one
from maps.Map_Two import map_two
from maps.Map_Three import map_three
from maps.Map_Four import map_four
from maps.Map_Five import map_five

from maps.Map_Six import map_six
from maps.Map_Seven import map_seven
from maps.Map_Eight import map_eight
from sprites import Wall_Sprite



class Simulation():
    shade_dict = {'C': 4,  # it is C for map eight!!! blank for rest
                  'W': 3,
                  'R': 2,
                  'G': 1,
                  ' ': 4}

    key_press_dict = {'a': key_press_a,
                      'd': key_press_d,
                      'w': key_press_w,
                      's': key_press_s,
                      'q': key_press_q,
                      'e': key_press_e}

    def __init__(self, screen_width, screen_height, console_font_size, textured, hashed_map, step_size, matrix_wall, color_to_glyph_wall):
        self.screen_width = screen_width         # Console Screen Size X (columns)
        self.screen_height = screen_height        # Console Screen Size Y (rows)
        self.console_font_size = console_font_size
        self.textured = textured
        self.hashed_map = hashed_map
        self.step_size = step_size

        self.map_height = None
        self.map_width = None
        self.map = None
        self.map_path = None

        self.screen = [['0' for x in range(self.screen_width)] for y in range(self.screen_height)]  # Creating empty screen matrix
        self.hashed_map_dict = {}
        self.hashed_screen = None

        self.player_x = None
        self.player_y = None
        self.player_a = 0.0             # Player Start Rotation

        self.player_radians_list = [0.00, 1.57, 3.14, 4.71]                          # Player angle
        self.player_radian_index = 0
        self.fov = 3.14159 / 4.0        # Field of View
        self.depth = 16.0               # Maximum rendering distance
        self.speed = 5.0                # Walking Speed
        
        self.tp1 = None
        self.tp2 = None
        
        self.wall = Sprite(matrix_wall, color_to_glyph_wall) # Initialize Sprite
        self.view = None

        self.elapsed_time = None

    def on_user_create(self):
        # hashed maps only designed for textures
        if self.hashed_map:
            self.textured == True
            # Checking if map file exists
            if os.path.exists(self.map_path):
                print('Loading in map...')
                # Opening JSON file
                f = open(self.map_path)
                
                # returns JSON object as
                # a dictionary
                self.hashed_map_dict = json.load(f)
                
                # Closing file
                f.close()
    
        
            else:
                # Have to create hashed map
                print('The hashed map specified does not exist...')

        # Create Screen Buffer and enable color on os
        os.system(f"mode con: cols={self.screen_width} lines={self.screen_height}")
        os.system('color')

        # Command Line Formatting (pixel size)
        command_line_font(self.console_font_size)

        # Inializing Curses
        self.view = curses.initscr()
        curses.curs_set(False)    # disables blinking curser
        curses.start_color()      # enables color
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)

        # Initiat time variables
        self.tp1 = time.perf_counter()
        self.tp2 = time.perf_counter()




    def on_key_press(self, key_pressed):
        self.player_a, self.player_y, self.player_x, self.player_radian_index = self.key_press_dict[key_pressed](self.player_a,
                                                                                                                 self.player_y, 
                                                                                                                 self.player_x, 
                                                                                                                 self.player_radian_index, 
                                                                                                                 self.hashed_map, 
                                                                                                                 self.player_radians_list, 
                                                                                                                 self.speed, 
                                                                                                                 self.elapsed_time,
                                                                                                                 self.map)

    
    def update_map(self, new_map, map_name):

        self.map = new_map
        self.map_height = len(self.map)
        self.map_width = len(self.map[0])
        self.map_path = 'Hashed_Maps/{}.json'.format(map_name)
        # Setting Player start position and processing map
        for row, list in enumerate(self.map):
            for col, value in enumerate(list):
                if value == 'p':
                    self.player_x = float(col) + 0.5
                    self.player_y = float(row) + 0.5
                    self.map[row][col] = '.'


    def on_user_update(self):

        # We'll need time differential per frame to calculate modification
        # to movement speeds, to ensure consistant movement, as ray-tracing
        # is non-deterministic
        self.tp2 = time.perf_counter()
        self.elapsed_time = self.tp2 - self.tp1
        self.tp1 = self.tp2
        self.elapsed_time = self.elapsed_time

        # Player input commands
        if keyboard.is_pressed('A'):                        # Move Leftwards
            self.on_key_press('a')
        elif keyboard.is_pressed('D'):                      # Move Rigtwards
            self.on_key_press('d')
        elif keyboard.is_pressed('W'):                      # Move Forwards
            self.on_key_press('w')
        elif keyboard.is_pressed('S'):                      # Move Backwards
            self.on_key_press('s')
        elif keyboard.is_pressed('Q'):                      # Turn Left
            self.on_key_press('q')
        elif keyboard.is_pressed('E'):                      # Turn Right
            self.on_key_press('e')
        elif keyboard.is_pressed('P'):                      # End Program
            curses.endwin()                                 # End curses instance
            os.system(f"mode con: cols={120} lines={40}")   # Reset screen buffer
            command_line_font(16)                           # Reset default font size
            del self.hashed_screen                          # Delete large memory object
            sys.exit()                                      # Exit Program

    


        # Get current screen
        # if self.hashed_map:
        # screen_string = self.hashed_map_dict.get("({}, {}, {})".format(round(self.player_a, 2), round(self.player_y, 1), round(self.player_x, 1)))
        # # try:

        # screen_list = [char for char in screen_string]
        # index = 0
        # for char in screen_list:
        #     coord_str = str(index / self.screen_width)
        #     coord_str = coord_str.split('.')
        #     y, x = coord_str[0], '0.' + coord_str[1]
        #     index = index + 1
        #     y = int(y)
        #     x = int(float(x) * self.screen_width)
        #     self.view.addstr(y, x, ' ', curses.color_pair(self.shade_dict[char]))
        # self.view.refresh()
        # w_key = False
        # s_key = False
        # a_key = False
        # d_key = False

            # except:
            #     # moved into non existing coord. move back to previous posistion
            #     if w_key:
            #         self.player_x -= math.sin(self.player_a) * self.speed * self.elapsed_time
            #         self.player_y -= math.cos(self.player_a) * self.speed * self.elapsed_time
            #     if s_key:
            #         self.player_x += math.sin(self.player_a) * self.speed * self.elapsed_time
            #         self.player_y += math.cos(self.player_a) * self.speed * self.elapsed_time
            #     if a_key:
            #         self.player_x += math.sin(self.player_a + 1.57) * self.speed * self.elapsed_time
            #         self.player_y += math.cos(self.player_a + 1.57) * self.speed * self.elapsed_time
            #     if d_key:
            #         self.player_x += math.sin(self.player_a - 1.57) * self.speed * self.elapsed_time
            #         self.player_y += math.cos(self.player_a - 1.57) * self.speed * self.elapsed_time

            #     screen_string = self.hashed_map_dict.get("({}, {}, {})".format(round(self.player_a, 2), round(self.player_y, 1), round(self.player_x, 1)))
            #     screen_list = [char for char in screen_string]
            #     index = 0
            #     for char in screen_list:
            #         coord_str = str(index / self.screen_width)
            #         coord_str = coord_str.split('.')
            #         y, x = coord_str[0], '0.' + coord_str[1]
            #         index = index + 1
            #         y = int(y)
            #         x = int(float(x) * self.screen_width)
            #         self.view.addstr(y, x, ' ', curses.color_pair(self.shade_dict[char]))
            #     self.view.refresh()

        # elif self.textured:
        #     self.calculate_screen()
        #     self.screen[self.screen_height - 1][self.screen_width - 1] = ''
        #     screen_string =  ''.join(ele for sub in self.screen for ele in sub)
        #     screen_list = [char for char in screen_string]
        #     index = 0
        #     for char in screen_list:
        #         coord_str = str(index / self.screen_width)
        #         coord_str = coord_str.split('.')
        #         y, x = coord_str[0], '0.' + coord_str[1]
        #         index = index + 1
        #         y = int(y)
        #         x = int(float(x) * self.screen_width)
        #         self.view.addstr(y, x, ' ', curses.color_pair(self.shade_dict[char]))
        #     self.view.refresh()

        # else: # classic
        self.calculate_screen()
        self.screen[self.screen_height - 1][self.screen_width - 1] = ''

        # Display Stats
        stats = f'X={"%.2f" % self.player_x}, Y={"%.2f" % self.player_y}, A={"%.2f" % self.player_a}, FPS={"%.2f" % (1.0 / self.elapsed_time)}'
        stats_window = curses.newwin(1, len(stats) + 1, 0, 0)
        stats_window.addstr(0, 0, stats)
        stats_window.refresh()

        # Display Map
        for nx in range(0, self.map_width):
            for ny in range(0, self.map_width):

                self.screen[ny + 1][nx] = self.map[ny][nx]
                
        self.screen[int(self.player_y)+1][int(self.player_x)] = 'p'
        screen_string =  ''.join(ele for sub in self.screen for ele in sub)

        self.view.addstr(0, 0, screen_string)
        self.view.refresh()



    def calculate_screen(self):
        for x in range(0, self.screen_width):

            # For each column, calculate the projected ray angle into world space
            ray_angle = (self.player_a - self.fov/2.0) + (float(x) / float(self.screen_width)) * self.fov

            # Find distance to wall
            step_size = self.step_size         # Increment size for ray casting, decrease to increase
            distance_to_wall = 0     #                                      resolution

            hit_wall = False       # Set when ray hits wall block
            boundary = False      # Set when ray hits boundary between two wall blocks

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

                        if self.textured:
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
                    
                        else: # it is classic
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

            for y in range(0, self.screen_height):

                if self.textured:
                    # Each Row
                    if y < ceiling:
                        # Shading in C for ceiling
                        self.screen[y][x] = 'C'

                    elif y > ceiling and y <= floor: # Drawing Wall
                        if distance_to_wall < self.depth:
                            sample_y = (y - ceiling) / (floor - ceiling)
                            color = self.wall.sample_color(sample_x, sample_y)
                            self.screen[y][x] = color

                        else:
                            self.screen[y][x] = ' ' # too far don't render

                    else: # Floor
                        # Shading in G for ground
                        self.screen[y][x] = 'G'

                else: # it is classic

                     # Shader walls based on distance
                    shade = ' '
                    if distance_to_wall <= self.depth / 4.0:         shade = u'\u2588'     # Very Close
                    elif distance_to_wall < self.depth / 3.0:        shade = u'\u2593'
                    elif distance_to_wall < self.depth / 2.0:        shade = u'\u2592'
                    elif distance_to_wall < self.depth:              shade = u'\u2591'
                    else:                                            shade = ' '        # Too far away

                    if boundary:                                     shade = ' ' # Black it out

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


if __name__ == '__main__':

    # Initiate simpulation loop
    screen_width = 120
    screen_height = 40
    console_font_size = 16
    textured = False
    hashed_map = False
    step_size = 0.1
    matrix_wall = Wall_Sprite.matrix
    color_to_glyph_wall = Wall_Sprite.color_to_glyph
    game = Simulation(screen_width, screen_height, console_font_size,textured, hashed_map, step_size, matrix_wall, color_to_glyph_wall)

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

    # Initiate with map_six
    game.update_map(map_seven, 'map_seven')
    game.on_user_create()

    while True:
        game.on_user_update()

    # That's It!! - Tyler
