import os
import sys

# Path restructure for imports
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


class Simulation():
    '''This class houses that main simulation. The simulation can be run in classic mode,
       texture mode, hashed mode and hashed color mode
       
        Attributes:
            screen_width (int): the width of the outputed screen
            screen_height (int): the height of the ouptuted screen
            console_font_size (int): modifies the font size of command prompt (y-size)
            simulation_type (str): lists weather to run the simulation in classic mode, texture mode, or hashed mode
            step_size (float): the smaller the number the higher the texture resolution
            matrix_wall (array): Holds the texturing information of the wall sprite to be rendered
            color_to_glyph_wall (dict): Converts color information in matrix_wall to glyph characters
            greyscale (bool): When hashing is a switch to turn on/off color mode
            map_height (int): height of 2d map matrix
            map_width (int): width of 2d map matrix
            map (array): 2d matrix contarinting world information
            map_path (str): a path to dump and grab json objects
            screen (array): 2d matrix that is rendered to the outputed screen
            hashed_map_dict (dict): holds the hashed json object
            player_x (float): player x coordinate in 2d map matrix
            player_y (float): player y coordinate in 2d map matrix
            player_a (float): player angle in 2d map matrix
            player_radians_list (array): list of four possible player angles
            player_radian_index (int): index for current posistion in player_radians_list
            fov (int): defines the players field of view rendered to the screen
            depth (float): the max distance that a ray will be casted
            speed (float): the speed at which the player travels through 2d map matrix
            wall (obj): is an instance of the sprite class containing the wall sprite
            view (obj): is a curses instance for painting text output to the screen
            tp1 (float): timestamp for tracking elapsed_time
            tp2 (float): timestamp for tracking elapsed_time
            elapsed_time (float): the amount of time it took to loop through an iteration
            simulation_type_dict (dict): calls simulation type methods dependent on simulation_type
            shade_dict (dict): converts color strings to number inputs for curses coloring
            key_press_dict (dict): call movement functions when a given keyboard key is pressed

    '''
    shade_dict = {'C': 4,
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

    
    def __init__(self, screen_width, screen_height, console_font_size, simulation_type, step_size, matrix_wall, color_to_glyph_wall, greyscale=False):
        """
        The constructor for Simulation class.
  
        Parameters:
            screen_width (int): the width of the outputed screen
            screen_height (int): the height of the ouptuted screen
            console_font_size (int): modifies the font size of command prompt (y-size)
            simulation_type (str): lists weather to run the simulation in classic mode, texture mode, or hashed mode
            step_size (float): the smaller the number the higher the texture resolution
            matrix_wall (array): Holds the texturing information of the wall sprite to be rendered
            color_to_glyph_wall (dict): Converts color information in matrix_wall to glyph characters
            greyscale (bool): When hashing is a switch to turn on/off color mode    
        """
        
        self.screen_width = screen_width                # Console Screen Size X (columns)
        self.screen_height = screen_height              # Console Screen Size Y (rows)
        self.console_font_size = console_font_size
        self.simulation_type = simulation_type          # classic, textured, hashed
        self.step_size = step_size
        self.greyscale = greyscale 

        self.map_height = None
        self.map_width = None
        self.map = None
        self.map_path = None

        self.screen = [['0' for x in range(self.screen_width)] for y in range(self.screen_height)]      # Creating empty screen matrix
        self.hashed_map_dict = {}

        self.player_x = None
        self.player_y = None
        self.player_a = 0.0                                             # Player Start Rotation

        self.player_radians_list = [0.00, 1.57, 3.14, 4.71]             # Player angle
        self.player_radian_index = 0
        self.fov = 3.14159 / 4.0                                        # Field of View
        self.depth = 16.0                                               # Maximum rendering distance
        self.speed = 5.0                                                # Walking Speed
        
        self.wall = Sprite(matrix_wall, color_to_glyph_wall)            # Initialize Sprite
        self.view = None

        self.tp1 = None
        self.tp2 = None
        self.elapsed_time = None

        self.simulation_type_dict = {'classic': self.run_classic,
                                     'textured': self.run_textured,
                                     'hashed': self.run_hashed}


    def on_user_create(self):
        '''Initializing the simulation: map loading, screen buffer, font size, curses instance, and time'''

        # Loading in hashed map
        if self.simulation_type == 'hashed':
            # Checking if map file exists
            if os.path.exists(self.map_path):
                print('Loading in map...')
                f = open(self.map_path)
                self.hashed_map_dict = json.load(f)
                f.close()
                
            else:
                # Map not at located at path
                print('The hashed map specified does not exist...')

        # Command Line Formatting (pixel size)
        command_line_font(self.console_font_size)

        # Create Screen Buffer and enable color on os
        os.system(f"mode con: cols={self.screen_width} lines={self.screen_height}")
        os.system('color')

        # Inializing Curses
        self.view = curses.initscr()
        curses.curs_set(False)                                          # Disables blinking curser
        curses.start_color()                                            # Enables color
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_GREEN)     # Setting color pairs
        curses.init_pair(2, curses.COLOR_BLACK, curses.COLOR_RED)
        curses.init_pair(3, curses.COLOR_BLACK, curses.COLOR_WHITE)
        curses.init_pair(4, curses.COLOR_BLACK, curses.COLOR_BLACK) 
        curses.init_pair(5, curses.COLOR_WHITE, curses.COLOR_RED)       # For efficant texture rendering
        curses.init_pair(6, curses.COLOR_WHITE, curses.COLOR_BLACK)     # For grey scale texture rendering

        # Initiate time variables
        self.tp1 = time.perf_counter()
        self.tp2 = time.perf_counter()


    def update_map(self, new_map, map_name):
        ''' Loads in specified map for simulation
            
            Parameters:
                new_map (array): a 2d matrix containing world information
                map_name (str): string containing the maps name'''

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
        '''To be called in a loop updates the user screen based on user inputs'''

        # Calculate time differential per frame
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
            del self.hashed_map_dict                        # Delete large memory object
            sys.exit()                                      # Exit Program


        self.simulation_type_dict[self.simulation_type]()

    
    def on_key_press(self, key_pressed):
        '''Routes to functions given which input key was pressed. Calls the key_pressed_dict'''
        self.player_a, self.player_y, self.player_x, self.player_radian_index = self.key_press_dict[key_pressed](self.player_a,
                                                                                                                 self.player_y, 
                                                                                                                 self.player_x, 
                                                                                                                 self.player_radian_index, 
                                                                                                                 self.simulation_type, 
                                                                                                                 self.player_radians_list, 
                                                                                                                 self.speed, 
                                                                                                                 self.elapsed_time,
                                                                                                                 self.map)


    def run_classic(self):
        '''Running the Greyscale simulation "Classic" Version. Also contains map and stats'''

        # Calculate Screen
        self.calculate_screen()

        # Display Map
        for nx in range(0, self.map_width):
            for ny in range(0, self.map_width):

                self.screen[ny + 1][nx] = self.map[ny][nx]
                
        self.screen[int(self.player_y)+1][int(self.player_x)] = 'p'

        # Display Stats
        stats = [char for char in f'X={"%.2f" % self.player_x}, Y={"%.2f" % self.player_y}, A={"%.2f" % self.player_a}, FPS={"%.2f" % (1.0 / self.elapsed_time)}']
        for index in range(len(stats)):
            self.screen[0][index] = stats[index]

        # Display Frame (problem with the \0 in python 3.9. empty string also works. null termination only needed for c++ version)
        self.screen[self.screen_height - 1][self.screen_width - 1] = ''
        self.view.addstr(0, 0, ''.join(ele for sub in self.screen for ele in sub))
        self.view.refresh()


    def run_textured(self):
        '''Running the simulation with default Brick Texture'''

        # Calculate Screen
        self.calculate_screen()
        self.view.refresh()

    def run_hashed(self):
        '''Running the hashed simulation. Calling from a previously calculated hash for the current screen given player coordinates'''
        
        # Get current screen
        screen_string = self.hashed_map_dict.get("({}, {}, {})".format(round(self.player_a, 2), round(self.player_y, 1), round(self.player_x, 1)))

        # Try excempt statement for when a dictionary value grab fails
        try:
            # Convertin string to a list
            screen_list = [char for char in screen_string]

            # Rendering hash in greyscale
            if self.greyscale:
                # For efficency forming one large string for texured wall rendering
                wall_string = ''
                for char in screen_list:
                    if char == 'R':
                        wall_string = wall_string + u'\u2588'   # background color white
                    elif char == 'W':
                        wall_string = wall_string + ' '         # block color Black
                    elif char == 'G':
                        wall_string = wall_string + u'\u2592'   # Shaded Ground
                    else:
                        wall_string = wall_string + ' '         # Blacked out ceiling

                self.view.addstr(0, 0, wall_string, curses.color_pair(6)) # Color pair for black and white wall
                self.view.refresh()

            # Rendering has in full color
            else:
                # For efficency forming one large string for texured wall rendering
                wall_string = ''
                for char in screen_list:
                    if char == 'R':
                        wall_string = wall_string + ' '                     # background color red
                    elif char == 'W':
                        wall_string = wall_string + u'\u2588'               # block color white
                    else:
                        wall_string = wall_string + '$'                     # placeholder to maintain string length

                self.view.addstr(0, 0, wall_string, curses.color_pair(5))   # Color pair for red and white wall

                # Process for finding the ceiling, ground, and too far away string values in the list and preparing them for rendering
                index = 0
                input_string = ' '
                last_char = screen_list[0]
                last_y = 0
                last_x = 0
                for char in screen_list:
                    if char == 'R' or char == 'W':                  # Ignoring all ready rendered red and white texture strings
                        if last_char == 'R' or last_char == 'W':
                            index = index + 1
                        else:
                            # Only rendering strings if the next value is not of the same color (optimizing for calling the self.view.addstr() the least amount of times possible)
                            self.view.addstr(last_y, last_x, input_string, curses.color_pair(self.shade_dict[last_char]))   # Add pixle to screen
                            input_string = ' '
                            last_char = char
                            last_y = y
                            last_x = x
                            index = index + 1
                    
                    else:
                        coord_str = str(index / self.screen_width)      # Calculating where char coord is in 2d matrix screen since 
                        coord_str = coord_str.split('.')                # currently chars exist in 1d array
                        y, x = coord_str[0], '0.' + coord_str[1]
                        y = int(y)
                        x = int(float(x) * self.screen_width)

                        if char == last_char:                           # Saving string of similar pixles for more efficent rendering
                            input_string = input_string + ' '
                        else:
                            # Only rendering strings if the next value is not of the same color (optimizing for calling the self.view.addstr() the least amount of times possible)
                            self.view.addstr(last_y, last_x, input_string, curses.color_pair(self.shade_dict[last_char]))   # Add pixle to screen
                            input_string = ' '
                            last_char = char
                            last_y = y
                            last_x = x

                        index = index + 1
                        
                self.view.addstr(last_y, last_x, input_string, curses.color_pair(self.shade_dict[last_char]))   # Add last long ground string to the screen
                self.view.refresh()                                                                             # Refreshing the screen

        # If the value grab fails move player back to previous location given the direction the player moved
        except:
            if keyboard.is_pressed('D'):
                self.player_x += math.sin(self.player_a - 1.57) * self.speed * self.elapsed_time
                self.player_y += math.cos(self.player_a - 1.57) * self.speed * self.elapsed_time
            elif keyboard.is_pressed('A'):
                self.player_x += math.sin(self.player_a + 1.57) * self.speed * self.elapsed_time
                self.player_y += math.cos(self.player_a + 1.57) * self.speed * self.elapsed_time
            elif keyboard.is_pressed('W'):
                self.player_x -= math.sin(self.player_a) * self.speed * self.elapsed_time
                self.player_y -= math.cos(self.player_a) * self.speed * self.elapsed_time
            elif keyboard.is_pressed('S'):
                self.player_x += math.sin(self.player_a) * self.speed * self.elapsed_time
                self.player_y += math.cos(self.player_a) * self.speed * self.elapsed_time


    def calculate_screen(self):
        '''Methode called for preforming ray casting. returns the current screen to be displayed
           given current simulation state'''

        # For each column of the screen
        for x in range(0, self.screen_width):

            # For each column, calculate the projected ray angle into world space
            ray_angle = (self.player_a - self.fov/2.0) + (float(x) / float(self.screen_width)) * self.fov

            # Find distance to wall
            step_size = self.step_size      # Increment size for ray casting, decrease to increase resolution
            distance_to_wall = 0                                   

            hit_wall = False                # Set when ray hits wall block
            boundary = False                # Set when ray hits boundary between two wall blocks

            eye_x = math.sin(ray_angle)     # Unit vector for ray in player space
            eye_y = math.cos(ray_angle)

            # Incrementally cast ray from player, along ray angle, testing for 
            # intersection with a block
            while hit_wall == False and distance_to_wall < self.depth:

                distance_to_wall += step_size
                test_x = int(self.player_x + eye_x * distance_to_wall)
                test_y = int(self.player_y + eye_y * distance_to_wall)

                # Test if ray is out of bounds
                if test_x < 0 or test_x >= self.map_width or test_y < 0 or test_y >= self.map_height:

                    hit_wall = True                     # Just set distance to maximum depth
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

            # Shader walls based on distance
            shade = ' '
            if distance_to_wall <= self.depth / 4.0:         shade = u'\u2588'      # Wall is Close
            elif distance_to_wall < self.depth / 3.0:        shade = u'\u2593'
            elif distance_to_wall < self.depth / 2.0:        shade = u'\u2592'
            elif distance_to_wall < self.depth:              shade = u'\u2591'
            else:                                            shade = ' '            # Wall too far away

            if boundary:                                     shade = ' '            # Black it the out wall

            # Shading in rows of the current column
            for y in range(0, self.screen_height):

                # Each Row
                if y < ceiling:                                 # Shading in the ceiling
                    if self.simulation_type == 'classic':       # Simulation type classic
                        self.screen[y][x] = ' '

                    else:
                        self.view.addstr(y, x, ' ')             # Simulation type Textured 

                elif y > ceiling and y <= floor:                # Shading in the wall
                    if self.simulation_type == 'classic':       # Simulation type classic
                        self.screen[y][x] = shade

                    else:                                       # Simulation type Textured 
                        if distance_to_wall < self.depth:

                            sample_y = (y - ceiling) / (floor - ceiling)
                            color = self.wall.sample_color(sample_x, sample_y)

                            self.screen[y][x] = ' '                                                     # Setting to a blank space for coloring
                            self.screen[self.screen_height - 1][self.screen_width - 1] = ''             # Removeing last cell for curser

                            if color == 'R':
                                self.view.addstr(y, x, str(self.screen[y][x]), curses.color_pair(2))    # Shading Red
                            else:
                                self.view.addstr(y, x, str(self.screen[y][x]), curses.color_pair(3))    # Shading White
                        
                        else:
                           self.view.addstr(y, x, ' ')                                                  # Too far don't render
                else:                                                    # Shading in floor
                    if self.simulation_type == 'classic':                # Simulation type classic
                        # Shade floor based on distance
                        b = 1.0 - ((float(y) - self.screen_height/2.0) / (float(self.screen_height) / 2.0))
                        if b < 0.25:        shade_2 = '#'
                        elif b < 0.5:       shade_2 = 'x'
                        elif b < 0.75:      shade_2 = '.'
                        elif b < 0.9:       shade_2 = '-'
                        else:               shade_2 = " "
                        self.screen[y][x] = shade_2

                    else:
                        # Shading in as dark green pixle Textured                       # Shading ni floor
                        if x == self.screen_width - 1 and y == self.screen_height -1:
                            self.view.addstr(y, x, '')
                        else:
                            self.view.addstr(y, x, ' ', curses.color_pair(1))            # Shading Green

