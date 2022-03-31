import os
import sys
import keyboard
import curses
import numpy as np

from Command_Line_Font import command_line_font


command_line_font(16)        # Console ASCII font size
nScreenWidth = 120          # Console Screen Size X (columns)
nScreenHeight = 40          # Console Screen Size Y (rows)

# Create Screen Buffer
screen = [[' ' for x in range(nScreenWidth)] for y in range(nScreenHeight)]
os.system(f"mode con: cols={nScreenWidth} lines={nScreenHeight}") # Font mechanic(y is always twice as big as x)
view = curses.initscr()

def draw(x, y):
    screen[y][x] = '1'

int x, y, dx, dy, dx1, dy1, px, py, xe, ye, i;
dx = x2 - x1;
dy = y2 - y1;
dx1 = abs(dx);
dy1 = abs(dy);
px = 2 * dy1 - dx1;
py = 2 * dx1 - dy1;

def draw_line(x1, y1, x2, y2):
    dx - x2, - x1
    dy = y2 - y1
    dx1 = abs(dx)
    dy1 = abs(dy)
    px = 2 * dy1 - dx1




while 1:

    # Quit simulation
    if keyboard.is_pressed('Q'):
        curses.endwin()                                 # End curses instance
        os.system(f"mode con: cols={120} lines={40}")   # Reset screen buffer
        command_line_font(16)                           # Reset default font size
        sys.exit()                                      # Exit Program

    # Initialize points
    x1 = 40
    x2 = 45
    y1 = 5
    y2 = 35

    # Draw line into matrix
    draw_line(x1, y1, x2, y2)

    # Display Frame (problem with the \0 in python 3.9. empty string also works. null termination only needed for c++ version)
    screen[nScreenHeight - 1][nScreenWidth - 1] = ''
    view.addstr(0, 0, ''.join(ele for sub in screen for ele in sub))
    view.refresh()