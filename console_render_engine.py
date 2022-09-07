'''A engine to render ASCII characters to the command line'''

import os
import sys
import curses
from typing import List

import keyboard

import cmd_tools


class ConsoleRenderEngine:
    '''
    The ConsoleRenderEngine is a built up tool for drawing ASCII characters
    to the command line.

    Attributes:
        font_size (int): the font size of the cmd ASCII characters
        screen_width (int): the width of the cmd buffer
        screen_height (int): the height of the cmd buffer
        screen (2DArray): matrix containing ASCII values
        stdscr (curses obj): is manipulated to render to cmd
    '''

    def __init__(self, font_size: int, screen_width: int, screen_height: int):
        """
        The constructor for ConsoleRenderEngine.

        Parameters:
            font_size (int): the font size of the cmd ASCII characters
            screen_width (int): the width of the cmd buffer
            screen_height (int): the height of the cmd buffer
        """

        self.font_size = font_size
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.screen: List[List[int]] = None
        self.stdscr: curses.initscr() = None

        self.__on_user_create()


    def __on_user_create(self):

        cmd_tools.cmd_font(self.font_size)  # Set font size
        self.reset_screen()                 # reset screen matrix

        # Shape cmd buffer dimentions
        os.system(f"mode con: cols={self.screen_width*2} lines={self.screen_height}")

        self.stdscr = curses.initscr()      # Initialize curses window for cmd


    def on_user_destroy(self):
        '''Reset cmd properties'''
        curses.endwin()                                  # End curses instance
        os.system(f"mode con: cols={120} lines={40}")    # Reset cmd buffer
        cmd_tools.cmd_font(16)                           # Reset default font size


    def reset_screen(self):
        '''Fills screen matrix with blank ASCII characters'''
        self.screen = [[' ' for x in range(self.screen_width)] for y in range(self.screen_height)]


    def display_screen(self):
        '''Display the current screen matrix in curses window instance'''
        self.screen[self.screen_height - 1][self.screen_width - 1] = ''
        self.stdscr.addstr(0, 0, ''.join(ele + ele for sub in self.screen for ele in sub))
        self.stdscr.refresh()


    def __draw(self, x: int, y: int, char: str):
        # Check screen boundry
        if x < self.screen_width and y < self.screen_height:
            self.screen[y][x] = char


    def __draw_line(self, x1: int, y1: int, x2: int, y2: int, char: str):
        dx = x2 - x1
        dy = y2 - y1
        dx1 = abs(dx)
        dy1 = abs(dy)
        px = 2 * dy1 - dx1
        py = 2 * dx1 - dy1

        if dy1 <= dx1:
            if dx >= 0:
                x = x1
                y = y1
                xe = x2

            else:
                x = x2
                y = y2
                xe = x1
            self.__draw(x, y, char)
            for _ in range(x, xe):
                x += 1
                if px < 0:
                    px = px + 2 * dy1

                else:
                    if (dx < 0 and dy < 0) or (dx > 0 and dy > 0):
                        y = y + 1

                    else:
                        y = y - 1
                    px = px + 2 * (dy1 - dx1)
                self.__draw(x, y, char)

        else:
            if dy >= 0:
                x = x1
                y = y1
                ye = y2

            else:
                x = x2
                y = y2
                ye = y1
            self.__draw(x, y, char)
            for _ in range(y, ye):
                y += 1
                if py <= 0:
                    py = py + 2 * dx1

                else:
                    if (dx < 0 and dy < 0) or (dx > 0 and dy > 0):
                        x = x + 1

                    else:
                        x = x - 1
                    py = py + 2 * (dx1 - dy1)
                self.__draw(x, y, char)


    def draw_triangle(self, x1: int, y1: int, x2: int, y2: int, x3: int, y3: int, char: str):
        '''Draws tringle lines to screen based on coordinates'''
        self.__draw_line(x1, y1, x2, y2, char)
        self.__draw_line(x2, y2, x3, y3, char)
        self.__draw_line(x3, y3, x1, y1, char)


    def __fill_line(self, sx: int, ex: int, ny: int, char: str):
        for i in range(sx, ex+1):
            self.__draw(i,ny, char)


    def fill_triangle(self, x1: int, y1: int, x2: int, y2: int, x3: int, y3: int, char: str):
        '''Fills tringle in based on coordinates'''
        changed1 = False
        changed2 = False

        # Sort vertices
        if y1 > y2:
            y1, y2 = y2, y1 
            x1, x2 = x2, x1
        if y1 > y3:
            y1, y3 = y3, y1
            x1, x3 = x3, x1
        if y2 > y3:
            y2, y3 = y3, y2
            x2, x3 = x3, x2

        t1x = x1
        t2x = x1
        y = y1  # Starting points

        dx1 = int(x2 - x1)
        if dx1 < 0:
            dx1 = -dx1
            signx1 = -1
        else:
            signx1 = 1
        dy1 = int(y2 - y1)

        dx2 = int(x3 - x1)
        if dx2 < 0:
            dx2 = -dx2
            signx2 = -1
        else:
            signx2 = 1
        dy2 = int(y3 - y1)

        # Swap values
        if dy1 > dx1: 
            dx1, dy1 = dy1, dx1
            changed1 = True

        # Swap values
        if dy2 > dx2:
            dy2, dx2 = dx2, dy2
            changed2 = True

        e2 = int(dx2 >> 1)

        # Flat top, just process the second half
        if y1 != y2:

            e1 = dx1 >> 1

            for i in range(0, dx1):

                next1 = False
                next2 = False
                t1xp = 0
                t2xp = 0

                if t1x < t2x:
                    minx = t1x
                    maxx = t2x
                else:
                    minx = t2x
                    maxx = t1x

                # Process first line until y value is about to change
                while i < dx1:
                    i += 1
                    e1 += dy1
                    while e1 >= dx1:
                        e1 -= dx1
                        if changed1:
                            t1xp = signx1
                        else:
                            next1 = True
                            break

                    if next1:
                        break

                    if changed1:
                        break
                    else:
                        t1x += signx1

                # Next1
                # Process second line until y value is about to change
                while 1:
                    e2 += dy2
                    while e2 >= dx2:
                        e2 -= dx2
                        if changed2:
                            t2xp = signx2
                        else:
                            next2 = True
                            break

                    if next2:
                        break
                    if changed2:
                        break
                    else:
                        t2x += signx2

                # Next2
                if minx > t1x:
                    minx = t1x
                if minx > t2x:
                    minx = t2x
                if maxx < t1x:
                    maxx = t1x
                if maxx < t2x:
                    maxx = t2x

                # Draw line from min to max points found on the y
                self.__fill_line(minx, maxx, y, char)

                # Now increase y
                if not changed1:
                    t1x += signx1
                t1x += t1xp
                if not changed2:
                    t2x += signx2
                t2x += t2xp
                y += 1
                if y == y2:
                    break

        # Next
        # Second half
        dx1 = int(x3 - x2)
        if dx1 < 0:
            dx1 = -dx1
            signx1 = -1
        else:
            signx1 = 1
        dy1 = int(y3 - y2)
        t1x = x2

        # Swap values
        if dy1 > dx1:
            dy1, dx1 = dx1, dy1
            changed1 = True

        else:
            changed1 = False

        e1 = int(dx1 >> 1)

        for i in range(0, dx1 + 1):

            next3 = False
            next4 = False
            t1xp = 0
            t2xp = 0

            if t1x < t2x:
                minx = t1x
                maxx = t2x
            else:
                minx = t2x
                maxx = t1x

            # Process first line until y value is about to change
            while i < dx1:
                e1 += dy1
                while e1 >= dx1:
                    e1 -= dx1
                    if changed1:
                        t1xp = signx1 # t1x += signx1;
                        break
                    else:
                        next3 = True
                        break

                if next3:
                    break

                if changed1:
                    break
                else:
                    t1x += signx1
                if i < dx1:
                    i += 1

            # Next3
            # Process second line until y value is about to change
            while t2x != x3:
                e2 += dy2
                while e2 >= dx2:
                    e2 -= dx2
                    if changed2:
                        t2xp = signx2
                    else:
                        next4 = True
                        break

                if next4:
                    break

                if changed2:
                    break
                else:
                    t2x += signx2

            # Next4
            # if minx > t1x:    # Visual Glitch with t1x
            #     minx = t1x
            if minx > t2x:
                minx = t2x
            # if maxx < t1x:    # Visual Glitch with t1x
            #     maxx = t1x
            if maxx < t2x:
                maxx = t2x

            self.__fill_line(minx, maxx, y, char)
            if not changed1:
                t1x += signx1
            t1x += t1xp
            if not changed2:
                t2x += signx2
            t2x += t2xp
            y += 1
            if y > y3:
                return
