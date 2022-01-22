import os
import sys

script_dir = os.path.dirname( __file__ )
main_dir = os.path.join( script_dir, '..' )
sys.path.append( main_dir )

import math
import json
import numpy as np

from classes.Sprite_Class import Sprite
from sprites.Wall_Sprite import matrix
from sprites.Wall_Sprite import color_to_glyph

class Map_Hasher():

    def __init__(self, screen_width, screen_height, step_size):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.step_size = step_size                                                               # Increment size for ray casting, decrease to increase

        self.map_height = None
        self.map_width = None
        self.map = None
        self.map_path = None

        self.screen = [['0' for x in range(self.screen_width)] for y in range(self.screen_height)]  # Creating empty screen matrix

        self.player_radians_list = [0.00, 1.57, 3.14, 4.71]                                       # Player angle
        self.fov = 3.14159 / 4.0                                                                  # Field of View
        self.depth = 16.0                                                                         # Maximum rendering distance
            
        self.wall = Sprite(matrix, color_to_glyph)                                                # Initialize Sprite


    def update_map(self, new_map, map_name):

        self.map = new_map
        self.map_height = len(self.map)
        self.map_width = len(self.map[0])
        self.map_path = 'Hashed_Maps/{}.json'.format(map_name)
        
        # Setting Player start position and processing map
        for row, list in enumerate(self.map):
            for col, value in enumerate(list):
                if value == 'p':
                    self.map[row][col] = '.'


    def create_hashed_map(self):
        # Checking if map file exists
        if os.path.exists(self.map_path):
            print('Map filename already exists...')
            sys.exit()
    
        else:
            # Have to create hashed map
            print('Creating hashed map. This may take a while...')

        # Initialize dict
        hashed_map = {}

        # Traversing the entire map
        for radian_hash in self.player_radians_list:
            for y_hash in np.arange(0.0, self.map_height, 0.1):
                for x_hash in np.arange(0.0, self.map_width, 0.1):
                    

                    # If we are in a wall
                    if self.map[int(y_hash)][int(x_hash)] == '#':
                        # No need to was memory we will never be at this coord
                        pass
                    else:

                        for x in range(0, self.screen_width):

                            # For each column, calculate the projected ray angle into world space
                            ray_angle = (radian_hash - self.fov/2.0) + (float(x) / float(self.screen_width)) * self.fov

                            # Find distance to wall
                            distance_to_wall = 0

                            hit_wall = False       # Set when ray hits wall block

                            eye_x = math.sin(ray_angle) # Unit vector for ray in player space
                            eye_y = math.cos(ray_angle)

                            sample_x = 0.0 # How far across the texture are we going to sample

                            # Incrementally cast ray from player, along ray angle, testing for 
                            # intersection with a block
                            while hit_wall == False and distance_to_wall < self.depth:

                                distance_to_wall += self.step_size
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


                        self.screen[self.screen_height - 1][self.screen_width - 1] = ''
                        screen_string =  ''.join(ele for sub in self.screen for ele in sub)
                        # Saving screen value in hash table
                        hashed_map.update({'({}, {}, {})'.format(round(radian_hash, 2), round(y_hash, 1), round(x_hash, 1)): screen_string})


        # Saving the hashed map as json file for future use
        with open(self.map_path, "w") as outfile:
            json.dump(hashed_map, outfile)

        print('Map hashing has completed! saved to: ' + self.map_path)
        del hashed_map
        sys.exit()


