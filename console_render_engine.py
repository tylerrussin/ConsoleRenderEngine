'''A engine to render ASCII characters to the command line'''

# ctypes structures cause pylint no member error
# pylint: disable=no-member

from typing import List

import  windows_console


class ConsoleRenderEngine:
    '''
    The ConsoleRenderEngine is a tool for drawing ASCII characters
    to the command line with the Windows Console API.

    Attributes:
        font_size (int): the font size of the cmd ASCII characters
        screen_width (int): the width of the cmd buffer
        screen_height (int): the height of the cmd buffer
        screen (list): list containing ASCII characters and attributes
        console_output (int): std handle output to the console
        console_window (SmallRect): a C structure defining console size
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

        self.screen: List[windows_console.CharInfo] = self.reset_screen()
        self.console_output: int = windows_console.get_std_handle(-11)
        self.console_window = windows_console.SmallRect(0,0,1,1)


    def __font_info(self, font_width: int, font_height: int,
                    family=0, weight=400, name="Consolas") -> None:
        '''Set console font info'''

        maximum_window = False
        font_infoex = windows_console.ConsoleFontInfoex()
        font_infoex.cbSize = windows_console.ctypes.sizeof(font_infoex)
        font_infoex.nFont = 0
        font_infoex.dwFontSize.X = font_width
        font_infoex.dwFontSize.Y = font_height
        font_infoex.FontFamily = family       # FF_DONTCARE
        font_infoex.FontWeight = weight       # FW_NORMAL
        font_infoex.FaceName = name

        windows_console.set_current_console_fontex(self.console_output, maximum_window, font_infoex)


    def on_user_create(self) -> None:
        '''Construct the windows console to specified settings'''

        # SetConsoleWindowInfo
        windows_console.set_console_window_info(self.console_output, True, self.console_window)

        # SetConsoleScreenBufferSize
        coord = windows_console.Coord(self.screen_width, self.screen_height)
        windows_console.set_console_screen_buffer_size(self.console_output, coord)

        # SetConsoleActiveScreenBuffer
        windows_console.set_console_active_screen_buffer(self.console_output)

        # Set font information in console
        self.__font_info(self.font_size, self.font_size)

        # SetConsoleCursorInfor
        console_cursor_info = windows_console.ConsoleCursorInfo()
        console_cursor_info.bVisible = False
        windows_console.set_console_cursor_info(self.console_output, console_cursor_info)

        # SetConsoleWindowInfo
        self.console_window = windows_console.SmallRect(0, 0,
                                                        self.screen_width - 1,
                                                        self.screen_height - 1)

        windows_console.set_console_window_info(self.console_output, True, self.console_window)


    def on_user_destroy(self):
        '''Construct the windows console to default settings'''
        original_width = 120
        original_height = 40
        original_font_width = 8
        original_font_height = 16

        self.console_window = windows_console.SmallRect(0,0,1,1)
        windows_console.set_console_window_info(self.console_output, True, self.console_window)

        coord = windows_console.Coord(original_width, original_height)
        windows_console.set_console_screen_buffer_size(self.console_output, coord)

        self.__font_info(original_font_width, original_font_height)

        self.console_window = windows_console.SmallRect(0, 0,
                                                        original_width - 1,
                                                        original_height - 1)

        windows_console.set_console_window_info(self.console_output, True, self.console_window)


    def reset_screen(self):
        '''Fills screen char info list with blank ASCII characters'''
        char = windows_console.Char(' ')
        cell_count = self.screen_width * self.screen_height
        self.screen = [windows_console.CharInfo(char, 0) for _ in range(cell_count)]


    def display_screen(self):
        '''Draws the curent screen char info list to console buffer'''

        self.screen[self.screen_width * self.screen_height - 1].Char.UnicodeChar = '\0'
        seq = windows_console.CharInfo * len(self.screen)
        windows_console.write_console_output_w(self.console_output, seq(*self.screen),
                                               windows_console.Coord(self.screen_width,
                                                                     self.screen_height),
                                               windows_console.Coord(0,0), self.console_window)


    def __draw(self, x: int, y: int, char: str):
        # Check screen boundry
        if x < self.screen_width and y < self.screen_height:
            self.screen[y * self.screen_width + x].Char.UnicodeChar = char
            self.screen[y * self.screen_width + x].Attributes = 0x000F


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
